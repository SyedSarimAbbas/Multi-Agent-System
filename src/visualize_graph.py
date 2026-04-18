import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import graph

def save_graph_image(output_path="graph.png"):
    print("\n[Visualization] Generating multi-agent graph...")
    
    # 1. ASCII Print (Immediate terminal feedback)
    try:
        print("\nMulti-Agent Graph (ASCII):")
        print("-" * 40)
        graph.get_graph().print_ascii()
        print("-" * 40)
    except Exception as e:
        print(f"Could not print ASCII graph: {e}")

    # 2. PNG Export
    try:
        # Generate the PNG bytes
        png_bytes = graph.get_graph().draw_mermaid_png()
        
        # Save to file
        with open(output_path, "wb") as f:
            f.write(png_bytes)
        print(f"\nSuccess: Graph image saved to {output_path}")
        
    except Exception as e:
        print(f"\nError generating PNG: {e}")
        print("Note: PNG generation may require an internet connection or mermaid dependencies.")
        
        # 3. Mermaid Text Fallback
        try:
            mermaid_text = graph.get_graph().draw_mermaid()
            print("\nMermaid Diagram Source:")
            print("-" * 40)
            print(mermaid_text)
            print("-" * 40)
            print("You can paste this into https://mermaid.live/ to view.")
        except Exception as e2:
            print(f"Failed to generate Mermaid text: {e2}")

if __name__ == "__main__":
    save_graph_image()
