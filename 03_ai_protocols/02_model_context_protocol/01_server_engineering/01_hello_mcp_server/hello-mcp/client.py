import httpx
import json
import asyncio

# --- Helper Function to Make MCP Requests ---
async def _mcp_request(method: str, params: dict = None):
    """A simple, reusable function to make JSON-RPC requests to our MCP server."""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1 # A static ID is fine for these simple, sequential examples
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            print(f"   -> Sending {method} request...")
            response = await client.post("http://localhost:8000/mcp/", json=payload, headers=headers)
            response.raise_for_status()
            print("RAW RESPONSE: ", type(response.text), response.text)
            # The server sends back SSE, so we parse it to get the JSON data
            for line in response.text.strip().split('\n'):
                print("LINE: ", line)
                if line.startswith('data: '):
                    return json.loads(line[6:])
            return {"error": "No data found in SSE response"}
        except Exception as e:
            print(f"   -> An error occurred: {e}")
            return {"error": str(e)}

# --- Main Demonstration ---
async def main():
    """A step-by-step demonstration of our first MCP client."""
    print("--- Hello MCP World: A Simple Client ---")
    
    # 1. List available tools
    print("\n[Step 1: Ask the server what it can do]")
    print("We send a 'tools/list' request to discover available tools.")
    tools_response = await _mcp_request("tools/list")
    
    if 'error' in tools_response:
        print(f"   -> Error listing tools: {tools_response['error']}")
        return
        
    tools = tools_response.get('result', {}).get('tools', [])
    if not tools:
        print("   -> The server didn't return any tools.")
        return
        
    print(f"   -> Success! The server has one tool:")
    tool_name = tools[0].get('name')
    tool_desc = tools[0].get('description')
    print(f"      - {tool_name}: {tool_desc.strip()}")

    # 2. Call the 'get_forecast' tool
    print(f"\n[Step 2: Use the '{tool_name}' tool]")
    city = "New York"
    print(f"Now, we'll call the tool to get the weather for '{city}'.")
    call_params = {"name": tool_name, "arguments": {"city": city}}
    call_response = await _mcp_request("tools/call", call_params)
    
    if 'error' in call_response:
        print(f"   -> Error calling '{tool_name}': {call_response['error']}")
    else:
        result = call_response.get('result', {}).get('content', [{}])[0].get('text')
        print(f"   -> Success! The server's response: '{result}'")
        
    print("\n--- Demonstration Complete ---")

if __name__ == "__main__":
    asyncio.run(main())