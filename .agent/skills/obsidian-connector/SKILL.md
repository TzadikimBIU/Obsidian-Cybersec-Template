---
name: obsidian-connector
description: Checks changes, active status, and note contents in the active Obsidian Electron app via CDP and REST API.
---

# Obsidian Connector Skill

This skill allows the agent to communicate directly with your active Obsidian application at runtime to see what note is open, read contents, query databases, or execute interface commands.

## Prerequisites

Before utilizing this skill, the following settings must be active:

1. **Local REST API**: The community plugin `Local REST API` must be installed and enabled in your Obsidian application. A `.env` file must exist at your vault root containing:
   ```text
   OBSIDIAN_REST_TOKEN=<your_generated_api_token>
   ```
2. **CDP Port**: Obsidian must be launched with the remote debugging port open:
   ```powershell
   & "C:\Path\To\Obsidian.exe" --remote-debugging-port=9222
   ```

---

## Usage Guide

### 1. Identify Which Note is Currently Open
To check which file the user is actively viewing/editing:
```bash
python ".agent/skills/obsidian-connector/obsidian_rest.py" get-active
```

### 2. Read Note Contents Programmatically
To fetch the Markdown content of an open note or any note inside the vault (e.g., `000 Home MOC.md`):
```bash
python ".agent/skills/obsidian-connector/obsidian_rest.py" read-note "000 Home MOC.md"
```

### 3. Run a Global Vault Search
To run a search across the entire vault using Obsidian's index:
```bash
python ".agent/skills/obsidian-connector/obsidian_rest.py" search "homework"
```

### 4. Execute an Obsidian Command Palette Action
To run any internal Obsidian action (e.g., manual HTML export, save, or rebuild indexes):
1. First, list all commands:
   ```bash
   python ".agent/skills/obsidian-connector/obsidian_rest.py" list-commands
   ```
2. Identify the target `commandId` (e.g., `webpage-html-export:export-vault`) and run it:
   ```bash
   python ".agent/skills/obsidian-connector/obsidian_rest.py" run-command "webpage-html-export:export-vault"
   ```

### 5. Inspect the Live Rendered DOM or Visual UI (CDP Mode)
To check the visual state of the notes, verify that Dataview rendered successfully, or inspect elements:
1. Verify if the debugging port is open:
   ```bash
   uv run python ".agent/skills/obsidian-connector/obsidian_cdp.py" status
   ```
2. Fetch the title and URL of the active Obsidian workspace tab:
   ```bash
   uv run python ".agent/skills/obsidian-connector/obsidian_cdp.py" active-view
   ```
3. Scrape the active editor's HTML or execute Javascript:
   ```bash
   uv run python ".agent/skills/obsidian-connector/obsidian_cdp.py" eval "document.querySelector('.view-content').innerText"
   ```
