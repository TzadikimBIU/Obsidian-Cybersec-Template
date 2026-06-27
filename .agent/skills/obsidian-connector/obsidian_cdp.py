# /// script
# dependencies = [
#     "websocket-client",
# ]
# ///

#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error
import socket

# Try importing websocket, which is managed dynamically by uv
try:
    import websocket
except ImportError:
    websocket = None

CDP_HOST = "127.0.0.1"
CDP_PORT = 9222

# 1. Check if the CDP port is open
def check_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        s.connect((CDP_HOST, CDP_PORT))
        s.close()
        return True
    except Exception:
        return False

# 2. Get list of all debug targets
def get_targets():
    if not check_port():
        return {"error": f"Port {CDP_PORT} is closed. Make sure Obsidian is running with --remote-debugging-port={CDP_PORT}"}
    
    url = f"http://{CDP_HOST}:{CDP_PORT}/json"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"error": "Failed to fetch targets from CDP", "reason": str(e.reason)}

# 3. Find the main Obsidian page target
def get_active_page_target(targets):
    if not isinstance(targets, list):
        return None
    for target in targets:
        if target.get("type") == "page":
            return target
    for target in targets:
        if "webSocketDebuggerUrl" in target:
            return target
    return None

# 4. Evaluate Javascript inside the target page using CDP WebSocket
def cdp_eval(js_expression):
    if websocket is None:
        return {"error": "websocket-client package is not installed. Please run this script with 'uv run' to automatically load dependencies."}
        
    targets = get_targets()
    if "error" in targets:
        return targets
        
    target = get_active_page_target(targets)
    if not target:
        return {"error": "No debuggable active page target found. Ensure Obsidian is open."}
        
    ws_url = target.get("webSocketDebuggerUrl")
    if not ws_url:
        return {"error": "No webSocketDebuggerUrl found for the target page."}
        
    try:
        ws = websocket.create_connection(ws_url, timeout=3.0)
    except Exception as e:
        return {"error": f"Failed to connect to DevTools WebSocket at {ws_url}", "reason": str(e)}
        
    cmd_id = 1
    payload = {
        "id": cmd_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_expression,
            "returnByValue": True
        }
    }
    
    try:
        ws.send(json.dumps(payload))
        while True:
            response_raw = ws.recv()
            response = json.loads(response_raw)
            if response.get("id") == cmd_id:
                ws.close()
                if "error" in response:
                    return {"error": "CDP execution error", "details": response["error"]}
                result = response.get("result", {})
                exc_details = result.get("exceptionDetails")
                if exc_details:
                    return {"error": "Javascript Exception", "details": exc_details.get("exception", {}).get("description")}
                return result.get("result", {})
    except Exception as e:
        ws.close()
        return {"error": "CDP WebSocket communication error", "reason": str(e)}

# 5. Router
def print_help():
    help_text = """
Obsidian CDP Client CLI
Usage:
  uv run python ".agent/skills/obsidian-connector/obsidian_cdp.py" status
  uv run python ".agent/skills/obsidian-connector/obsidian_cdp.py" active-view
  uv run python ".agent/skills/obsidian-connector/obsidian_cdp.py" eval <js_expression>
"""
    print(help_text)
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print_help()
        
    cmd = sys.argv[1]
    
    if cmd == "status":
        is_open = check_port()
        print(json.dumps({"port_9222_open": is_open}))
        
    elif cmd == "active-view":
        targets = get_targets()
        if "error" in targets:
            print(json.dumps(targets, indent=2))
            sys.exit(1)
        target = get_active_page_target(targets)
        if target:
            print(json.dumps({
                "title": target.get("title"),
                "url": target.get("url"),
                "id": target.get("id")
            }, indent=2))
        else:
            print(json.dumps({"error": "No active page target found."}))
            
    elif cmd == "eval":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing JavaScript expression. Usage: eval <js_expression>"}))
            sys.exit(1)
        js_expression = " ".join(sys.argv[2:])
        result = cdp_eval(js_expression)
        print(json.dumps(result, indent=2))
        
    else:
        print_help()

if __name__ == "__main__":
    main()
