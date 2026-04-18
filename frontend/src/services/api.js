const API_BASE = "http://127.0.0.1:8000";

export async function sendQuery(query) {
  const res = await fetch(`${API_BASE}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => "Unknown error");
    throw new Error(`Request failed (${res.status}): ${detail}`);
  }

  return res.json();
}

export async function streamQuery(query, onUpdate) {
  const response = await fetch(`${API_BASE}/api/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Stream request failed: ${detail}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    
    // Split by SSE message separator
    const lines = buffer.split("\n\n");
    buffer = lines.pop(); // Keep partial message in buffer

    for (const line of lines) {
      if (line.trim() === "") continue;
      
      const eventMatch = line.match(/^event: (.*)$/m);
      const dataMatch = line.match(/^data: (.*)$/m);
      
      if (eventMatch && dataMatch) {
        const event = eventMatch[1];
        const data = JSON.parse(dataMatch[1]);
        onUpdate({ event, data });
      }
    }
  }
}

export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return res.ok;
  } catch {
    return false;
  }
}
