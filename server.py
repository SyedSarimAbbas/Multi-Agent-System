import os
import sys
import io
import re
from contextlib import redirect_stdout

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.main import run_agent

app = FastAPI(title="Multi-Agent AI System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve graph.png as a static asset
if os.path.exists("graph.png"):
    app.mount("/static", StaticFiles(directory="."), name="static")


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str
    agent: str
    trace: list[str]


def parse_trace(captured: str) -> tuple[str, list[str]]:
    """Extract the agent name and step trace from captured stdout."""
    lines = [l.strip() for l in captured.strip().splitlines() if l.strip()]
    trace = []
    agent = "general"

    agent_map = {
        "weather": "weather",
        "calculator": "calculator",
        "crypto": "crypto",
        "general": "general",
    }

    for line in lines:
        if line.startswith("[Node:"):
            match = re.search(r"\[Node:\s*(\w+)\]", line)
            if match:
                node_name = match.group(1).lower()
                if node_name in agent_map:
                    agent = agent_map[node_name]
            trace.append(line)
        elif "Sending Prompt" in line or "Response Received" in line:
            trace.append(line)

    return agent, trace


@app.post("/api/query", response_model=QueryResponse)
async def handle_query(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            answer = run_agent(req.query)

        captured = buf.getvalue()
        agent, trace = parse_trace(captured)

        return QueryResponse(
            response=answer or "No response generated.",
            agent=agent,
            trace=trace,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
