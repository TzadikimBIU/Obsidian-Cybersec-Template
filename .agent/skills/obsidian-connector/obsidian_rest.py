#!/usr/bin/env python3
import os
import sys
import json
import ssl
import urllib.request
import urllib.parse

# 1. Load config from Environment or .env file
def load_config():
    config = {
        "PORT": "27124",
        "TOKEN": ""
    }
    
    # Read .env if it exists (4 levels up: .agent/skills/obsidian-connector/obsidian_rest.py)
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = parts[1].strip().strip('"').strip("'")
                        if key == "OBSIDIAN_REST_TOKEN":
                            config["TOKEN"] = val
                        elif key == "OBSIDIAN_REST_PORT":
                            config["PORT"] = val
                            
    # Environment variables take precedence
    if os.getenv("OBSIDIAN_REST_TOKEN"):
        config["TOKEN"] = os.getenv("OBSIDIAN_REST_TOKEN")
    if os.getenv("OBSIDIAN_REST_PORT"):
        config["PORT"] = os.getenv("OBSIDIAN_REST_PORT")
        
    return config

# 2. Make an authenticated API request
def make_request(path, method="GET", data=None, headers=None):
    config = load_config()
    if not config["TOKEN"]:
        print(json.dumps({"error": "OBSIDIAN_REST_TOKEN not found. Please set it in your .env file at the vault root."}))
        sys.exit(1)
        
    url = f"https://127.0.0.1:{config['PORT']}{path}"
    
    req_headers = {
        "Authorization": f"Bearer {config['TOKEN']}",
        "Content-Type": "application/json"
    }
    if headers:
        req_headers.update(headers)
        
    req_data = None
    if data is not None:
        if isinstance(data, (dict, list)):
            req_data = json.dumps(data).encode("utf-8")
        else:
            req_data = data.encode("utf-8")
            
    req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
    
    # Bypassing self-signed certificates used by the local REST API
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res_data = response.read()
            # Try to return parsed JSON, else string
            try:
                return json.loads(res_data.decode("utf-8"))
            except json.JSONDecodeError:
                return res_data.decode("utf-8")
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
            return {"error": f"HTTP {e.code}", "details": json.loads(err_body)}
        except Exception:
            return {"error": f"HTTP {e.code}", "reason": e.reason}
    except urllib.error.URLError as e:
        return {"error": "Connection failed. Is Obsidian running and Local REST API plugin enabled?", "reason": str(e.reason)}

# 3. Main Command Router
def print_help():
    help_text = """
Obsidian REST API Client CLI
Usage:
  python ".agent/skills/obsidian-connector/obsidian_rest.py" get-active
  python ".agent/skills/obsidian-connector/obsidian_rest.py" read-note <vault_path>
  python ".agent/skills/obsidian-connector/obsidian_rest.py" search <query_text>
  python ".agent/skills/obsidian-connector/obsidian_rest.py" list-commands
  python ".agent/skills/obsidian-connector/obsidian_rest.py" run-command <command_id>
"""
    print(help_text)
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print_help()
        
    cmd = sys.argv[1]
    
    if cmd == "get-active":
        result = make_request("/active")
        print(json.dumps(result, indent=2))
        
    elif cmd == "read-note":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing note path. Usage: read-note <vault_path>"}))
            sys.exit(1)
        path = sys.argv[2]
        # URL encode the vault path
        encoded_path = urllib.parse.quote(path)
        result = make_request(f"/vault/{encoded_path}", headers={"Accept": "text/markdown"})
        # If it returns a string, print it directly, otherwise print json (e.g. error)
        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, indent=2))
            
    elif cmd == "search":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing query text. Usage: search <query_text>"}))
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        result = make_request("/search", method="POST", data={"query": query})
        print(json.dumps(result, indent=2))
        
    elif cmd == "list-commands":
        result = make_request("/commands")
        print(json.dumps(result, indent=2))
        
    elif cmd == "run-command":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing command ID. Usage: run-command <command_id>"}))
            sys.exit(1)
        command_id = sys.argv[2]
        result = make_request(f"/commands/{command_id}", method="POST")
        print(json.dumps(result, indent=2))
        
    else:
        print_help()

if __name__ == "__main__":
    main()
