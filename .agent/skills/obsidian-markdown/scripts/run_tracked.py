#!/usr/bin/env python3
import os
import re
import sys
import json
import subprocess
import argparse

DEFAULT_BRAIN_DIR = r"C:\Users\thomy\.gemini\antigravity-ide\brain"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".tracker_state.json")

def get_walkthrough_path():
    if not os.path.exists(DEFAULT_BRAIN_DIR):
        return None
    subdirs = []
    for d in os.listdir(DEFAULT_BRAIN_DIR):
        full_path = os.path.join(DEFAULT_BRAIN_DIR, d)
        if os.path.isdir(full_path):
            # Check if directory name is a UUID (36 chars, hex and hyphens)
            if re.match(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", d):
                subdirs.append(full_path)
    if not subdirs:
        return None
    active_conv = max(subdirs, key=os.path.getmtime)
    return os.path.join(active_conv, "walkthrough.md")

def is_git_repository(path):
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], 
            cwd=path, 
            capture_output=True
        )
        return res.returncode == 0
    except Exception:
        return False

def get_external_snapshot(path):
    snapshot = {}
    if not path or not os.path.exists(path):
        return snapshot
    for root, dirs, files in os.walk(path):
        if any(p in root for p in [".git", "node_modules", ".obsidian/workspace.json", ".stfolder", ".stversions", ".trash"]):
            continue
        for file in files:
            if file == ".tracker_state.json":
                continue
            full_path = os.path.abspath(os.path.join(root, file))
            try:
                snapshot[full_path] = os.path.getmtime(full_path)
            except OSError:
                pass
    return snapshot

def get_diff_lines(path):
    try:
        res = subprocess.run(
            ["git", "diff", "-U0"], 
            cwd=path, 
            capture_output=True, 
            text=True, 
            check=True
        )
        diff_output = res.stdout
    except Exception as e:
        print(f"Failed to get git diff: {e}")
        return []

    changes = []
    current_file = None
    
    for line in diff_output.splitlines():
        if line.startswith("+++ b/"):
            current_file = os.path.abspath(os.path.join(path, line[6:]))
        elif line.startswith("@@ ") and current_file:
            match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if match:
                start = int(match.group(1))
                count = int(match.group(2)) if match.group(2) else 1
                end = start + count - 1 if count > 0 else start
                changes.append({
                    "file": current_file,
                    "start": start,
                    "end": end,
                    "status": "MODIFY"
                })
                
    # Add untracked files
    try:
        res_untracked = subprocess.run(
            ["git", "status", "--porcelain"], 
            cwd=path, 
            capture_output=True, 
            text=True, 
            check=True
        )
        for line in res_untracked.stdout.splitlines():
            if line.startswith("?? "):
                rel_path = line[3:]
                abs_path = os.path.abspath(os.path.join(path, rel_path))
                changes.append({
                    "file": abs_path,
                    "start": None,
                    "end": None,
                    "status": "NEW"
                })
    except Exception:
        pass
        
    return changes

def save_state(external_path, local_is_git, local_before, external_before):
    state = {
        "external_path": external_path,
        "local_is_git": local_is_git,
        "local_before": local_before,
        "external_before": external_before
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print("Tracking session started successfully.")
    except Exception as e:
        print(f"Failed to save tracking state: {e}")
        sys.exit(1)

def load_state():
    if not os.path.exists(STATE_FILE):
        print("No active tracking session found. Run with --start first.")
        sys.exit(1)
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to read tracking state: {e}")
        sys.exit(1)

def clear_state():
    if os.path.exists(STATE_FILE):
        try:
            os.remove(STATE_FILE)
        except Exception as e:
            print(f"Failed to remove state file: {e}")

def process_and_write(local_is_git, local_before, local_after, external_path, external_before, external_after):
    walkthrough = get_walkthrough_path()
    if not walkthrough:
        print("Could not find active walkthrough.md to write changes.")
        return
        
    print(f"Active Walkthrough: {walkthrough}")
    
    new_entries = []
    
    # 1. Process local changes
    if local_is_git:
        local_changes = get_diff_lines(".")
        for change in local_changes:
            file_path = change["file"]
            basename = os.path.basename(file_path)
            file_url = "file:///" + file_path.replace("\\", "/").replace(" ", "%20")
            status = change["status"]
            
            if change["start"] is not None:
                start = change["start"]
                end = change["end"]
                file_link = f"{file_url}#L{start}-L{end}"
                link_text = f"{basename}:L{start}-{end}"
            else:
                file_link = file_url
                link_text = basename
                
            new_entries.append(f"#### [{status}] [{link_text}]({file_link})")
    else:
        for file_path, mtime in local_after.items():
            basename = os.path.basename(file_path)
            file_url = "file:///" + file_path.replace("\\", "/").replace(" ", "%20")
            
            if file_path not in local_before:
                new_entries.append(f"#### [NEW] [{basename}]({file_url})")
            elif local_before[file_path] != mtime:
                new_entries.append(f"#### [MODIFY] [{basename}]({file_url})")
        
    # 2. Process external changes
    for file_path, mtime in external_after.items():
        basename = os.path.basename(file_path)
        file_url = "file:///" + file_path.replace("\\", "/").replace(" ", "%20")
        
        if file_path not in external_before:
            new_entries.append(f"#### [NEW] [{basename}]({file_url})")
        elif external_before[file_path] != mtime:
            new_entries.append(f"#### [MODIFY] [{basename}]({file_url})")
            
    # 3. Write to walkthrough.md
    if new_entries:
        try:
            with open(walkthrough, "r", encoding="utf-8") as f:
                content = f.read()
                
            filtered_entries = []
            for entry in new_entries:
                url_match = re.search(r"\(file:///.*?\)", entry)
                if url_match:
                    url = url_match.group(0)
                    if url not in content:
                        filtered_entries.append(entry)
                else:
                    filtered_entries.append(entry)
            
            if filtered_entries:
                with open(walkthrough, "a", encoding="utf-8") as f:
                    f.write("\n" + "\n".join(filtered_entries) + "\n")
                print(f"Registered {len(filtered_entries)} file/line modifications in walkthrough.")
            else:
                print("All detected changes were already registered in walkthrough.")
        except Exception as e:
            print(f"Failed to write to walkthrough: {e}")
    else:
        print("No file or line changes detected.")

def main():
    parser = argparse.ArgumentParser(description="Record file/line changes in IDE walkthrough.md via session or single execution.")
    parser.add_argument("--start", action="store_true", help="Start a new tracking session (snapshots folder states).")
    parser.add_argument("--stop", action="store_true", help="Stop tracking session and write accumulated changes.")
    parser.add_argument("--external", help="External directory path to watch for file-level changes.")
    parser.add_argument("cmd", nargs="*", help="The command to execute (for single-execution wrapping).")
    
    args = parser.parse_args()
    
    if args.start:
        if args.cmd:
            print("Error: Cannot pass command with --start. Start a session first, run commands, then use --stop.")
            sys.exit(1)
        local_is_git = is_git_repository(".")
        local_before = {} if local_is_git else get_external_snapshot(".")
        external_before = get_external_snapshot(args.external)
        save_state(args.external, local_is_git, local_before, external_before)
        sys.exit(0)
        
    elif args.stop:
        if args.cmd:
            print("Error: Cannot pass command with --stop.")
            sys.exit(1)
        state = load_state()
        local_is_git = state["local_is_git"]
        local_before = state["local_before"]
        external_path = state["external_path"]
        external_before = state["external_before"]
        
        local_after = {} if local_is_git else get_external_snapshot(".")
        external_after = get_external_snapshot(external_path)
        
        process_and_write(local_is_git, local_before, local_after, external_path, external_before, external_after)
        clear_state()
        sys.exit(0)
        
    else:
        # Backward-compatible single-execution wrapped command mode
        if not args.cmd:
            parser.print_help()
            sys.exit(1)
            
        local_is_git = is_git_repository(".")
        local_before = {} if local_is_git else get_external_snapshot(".")
        external_before = get_external_snapshot(args.external)
        
        print(f"Executing: {' '.join(args.cmd)}")
        try:
            res = subprocess.run(args.cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code: {e.returncode}")
            sys.exit(e.returncode)
            
        local_after = {} if local_is_git else get_external_snapshot(".")
        external_after = get_external_snapshot(args.external)
        
        process_and_write(local_is_git, local_before, local_after, args.external, external_before, external_after)

if __name__ == "__main__":
    main()
