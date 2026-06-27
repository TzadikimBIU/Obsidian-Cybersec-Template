# 🧠 AI Guide & Vault System Rules

This file is a system reference and instruction guide for any AI assistants, Copilot plugins, or agents (e.g., Cursor, Cliner, Gemini, Copilot) interacting with this Obsidian Vault. It ensures all AI-generated content conforms to the vault's structure, metadata design, and automation workflows.

---

## 📂 Vault Folder Directory Structure

The vault is organized into numbered folders representing specific cybersecurity research areas:

```
Vault Root/
│
├── 000 Home MOC.md                    # Cybersecurity Command Center Dashboard
│
├── 001 Daily Logs/                    # Session journals and daily logs
│
├── 010 Engagements/                   # Pentests, red team ops, bug bounty
│   ├── Active/                        # Ongoing engagements
│   │   └── <Client Name>/             # Specific client folder
│   │       ├── <Client> MOC.md        # Client Home Dashboard
│   │       ├── Findings/              # Auto-numbered vulnerability findings (FIND-NNN)
│   │       ├── Recon/                 # Host discovery and intelligence gathering notes
│   │       ├── Scans/                 # Port scans and vulnerability scans (Nmap, Nessus)
│   │       ├── Exploitation/          # Exploit attempts and PoC notes
│   │       └── Artifacts/             # Evidence files, scripts, and logs
│   └── Archive/                       # Completed engagements
│
├── 011 CTF/                           # CTF Writeups
│   └── <CTF Event Name>/              # Specific event writeups sorted by category
│
├── 012 Vuln Research/                 # Target-specific vulnerability research
│
├── 013 Topic Research/                # Self-directed security domain research
│   └── <Topic Name>/                  # e.g., Anti-Reverse Engineering
│       ├── <Topic> MOC.md             # Topic research outline & reading list
│       ├── Experiments/               # PoCs and code experiments
│       └── Papers & References/       # Reference PDFs and advisories
│
├── 020 Threat Intel/                  # APT groups, campaigns, and IOCs
│
├── 021 Malware Analysis/              # Sample-specific reverse engineering sessions
│   └── <Sample Name>/                 # Specific malware sample folder
│
├── 030 Tools/                         # Tool cheatsheets, one-liners, and configs
│
├── 040 Knowledge Base/                # Permanent MITRE-mapped technique notes
│
├── 050 References/                    # CVEs, academic papers, and security advisories
│
├── 060 Labs/                          # Lab machines (HTB, THM, VulnHub, Home Lab)
│
├── 070 Reporting/                     # Report templates and deliverables
│
├── 080 DFIR/                          # Incident response cases and playbooks
│   ├── Cases/                         # Incident case files (INC-NNN)
│   └── Playbooks/                     # IR playbooks for threat vectors
│
├── 090 System/                        # System configurations, templates & scripts
│   └── 000 Templates/                 # Templater templates and automation scripts
│
└── copilot/                           # AI Copilot plugin data (conversations, custom prompts)
```

---

## 🏷️ Metadata Frontmatter Schemas

Every note in the vault must contain valid YAML frontmatter matching its note type. Never erase or omit these fields when writing or editing notes.

### 1. Sovereign MOC (Home Command Center)
* **Path:** `000 Home MOC.md`
```yaml
---
type: sovereign_moc
researcher_name: ""
cssclasses:
  - home-moc
---
```

### 2. Engagement MOC (Individual Client Home)
* **Path:** `010 Engagements/Active/<Client>/<Client> MOC.md`
```yaml
---
type: engagement_moc
client: "<Client Name>"
scope: []
start_date: YYYY-MM-DD
end_date: ""
status: active                 # active, completed, on-hold
engagement_type: external_pentest  # external_pentest, internal_pentest, web_app, red_team
cvss_critical: 0
cvss_high: 0
cvss_medium: 0
cvss_low: 0
cvss_info: 0
tags:
  - engagement
---
```

### 3. Finding Note
* **Path:** `010 Engagements/Active/<Client>/Findings/FIND-NNN <Title>.md`
```yaml
---
type: finding
engagement: "[[<Client> MOC]]"
title: "FIND-NNN <Title>"
severity: high                 # critical, high, medium, low, info
cvss: 0.0
cvss_vector: ""
status: draft                  # draft, ready, confirmed
cwe: "CWE-XX"
affected_component: ""
date_found: YYYY-MM-DD
tags:
  - finding
---
```

### 4. CTF Challenge Note
* **Path:** `011 CTF/<Event>/<Challenge>.md`
```yaml
---
type: ctf_challenge
ctf: "<Event Name>"
category: web                  # web, pwn, rev, crypto, forensics, misc
difficulty: medium             # easy, medium, hard
points: 0
solved: false
flag: ""
real_world_cve: ""
technique_link: "[[]]"
tags:
  - ctf
---
```

### 5. Lab Machine Writeup
* **Path:** `060 Labs/<Platform>/<Machine>.md`
```yaml
---
type: lab_machine
platform: hackthebox           # hackthebox, tryhackme, vulnhub, homelab
machine: "<Machine Name>"
os: linux                      # linux, windows, active_directory
difficulty: medium
ip: ""
user_flag: ""
root_flag: ""
status: in-progress            # in-progress, completed
tags:
  - lab
---
```

### 6. Malware Analysis Session
* **Path:** `021 Malware Analysis/<Sample>/<Sample> Analysis.md`
```yaml
---
type: malware_analysis
malware_name: "<Sample Name>"
family: ""
sha256: ""
md5: ""
first_seen: YYYY-MM-DD
platform: ""                   # windows, linux, android
packer: ""
c2: []
mitre_attack: []
sandbox_report: ""
status: in-progress            # in-progress, completed
tags:
  - malware
  - reversing
---
```

### 7. DFIR Case MOC
* **Path:** `080 DFIR/Cases/INC-NNN <Description>/INC-NNN MOC.md`
```yaml
---
type: dfir_case
case_id: "INC-NNN"
description: "<Description>"
severity: high                 # critical, high, medium, low
date_opened: YYYY-MM-DD
date_closed: ""
status: open                   # open, closed, containment
tags:
  - dfir
  - incident
---
```

### 8. Topic Research MOC
* **Path:** `013 Topic Research/<Topic>/<Topic> MOC.md`
```yaml
---
type: topic_research_moc
topic: "<Topic Name>"
status: active                 # active, completed
started: YYYY-MM-DD
last_updated: YYYY-MM-DD
research_questions: []
related_malware: []
related_techniques: []
tags: []
---
```

### 9. Daily Log
* **Path:** `001 Daily Logs/YYYY-MM-DD.md`
```yaml
---
type: daily_log
date: YYYY-MM-DD
active_engagements: []
hours_logged: 0
tags:
  - daily-log
---
```

---

## 🛠️ Note Creation & Automation Workflows

The vault utilizes **Templater** for automating note creation. AI assistants should prefer instructing users to run Templater scripts rather than creating files manually.

1. **Active Automation Scripts**:
   - `New Engagement Script.md` -> Scaffolds `010 Engagements/Active/<Client>` with full subfolders and initializes the `MOC` note.
   - `New Finding Script.md` -> Counts existing findings and generates an auto-numbered `FIND-NNN <title>.md` under the active engagement.
   - `New Topic Research Script.md` -> Scaffolds `013 Topic Research/<Topic>` with Experiments and Papers directories + MOC.
   - `New Malware Analysis Script.md` -> Scaffolds reversing folders + MOC for a new sample.
   - `New CTF Script.md` -> Creates a CTF challenge note routed to the correct folder.
   - `New DFIR Case Script.md` -> Scaffolds `INC-NNN` folder with MOC, Timeline, and IOCs notes.
   - `New Lab Machine Script.md` -> Sets up lab writeups inside `060 Labs`.
   - `New CVE Script.md` -> Adds a CVE reference note under `050 References/CVEs`.
   - `Smart Sec Note Creator.md` -> Run this inside an Engagement MOC or Topic Research MOC. It auto-detects MOC context and creates appropriate subnotes (Recon, Scans, Experiments).
   - `Generate Report Script.md` -> Run this inside an Engagement MOC to aggregate all its findings into a report outline or full draft.

---

## 🔌 Live App Connection (AI Connector)

This vault includes a live-running connection interface located in [`.agent/skills/obsidian-connector/`](file:///c:/Users/thomy/Obsidian%20notes/.agent/skills/obsidian-connector/). If you are running as an AI agent (e.g. Cursor, Gemini, Cliner) inside this vault, you can query the active Obsidian instance directly to read state, verify rendering, or run actions using these scripts:

* **Check active note path**: `python ".agent/skills/obsidian-connector/obsidian_rest.py" get-active`
* **Read file content**: `python ".agent/skills/obsidian-connector/obsidian_rest.py" read-note "<vault_path>"`
* **Execute command**: `python ".agent/skills/obsidian-connector/obsidian_rest.py" run-command "<command_id>"`
* **Inspect live visual DOM**: `uv run python ".agent/skills/obsidian-connector/obsidian_cdp.py" eval "<js_expression>"`

Refer to the custom skill definition in [`SKILL.md`](file:///c:/Users/thomy/Obsidian%20notes/.agent/skills/obsidian-connector/SKILL.md) for full setup instructions (requires the Local REST API plugin and/or starting Obsidian with debug port 9222).

---

## 🤖 AI Guidelines & Best Practices

When generating text, modifying files, or creating new content in this vault, AI must adhere to these guidelines:

* **Use Obsidian Link Formatting:** Always link to other notes or subjects using double brackets: `[[Note Name]]`. Do not use markdown URLs for internal vault links.
* **Preserve Frontmatter:** Never modify frontmatter properties unless explicitly requested (e.g. updating finding severity or setting a CVE exploit link). Ensure you do not change existing dates or types.
* **Respect Dashboard Views:** The Home MOC utilizes Dataview tables for live operations tracking. Ensure files are correctly tagged (e.g., `type: finding`, `solved: false`) so they are auto-aggregated.
* **Lotus Code Block Execution:** The vault supports Lotus for live code block execution. If demonstrating security scripts, command-line usage, or PoCs, make sure to add `lotus-execution=<group>` parameters (e.g. `lotus-execution=docker_pentest` or `lotus-execution=native`).
* **Use Premium Callout Layouts:** When requested to style or structure MOCs, use multi-column callouts (e.g. `> [!multi-column]`) and standard Obsidian alert blocks (e.g. `> [!info]`, `> [!abstract]`, `> [!warning]`) to keep dashboards visually stunning.

---

## VERIFICATION & ARTIFACTS
- To register file modifications and line-level edits on the IDE tracking pane, you must use the tracking session utility.
- **Start tracking** at the very beginning of your task execution phase:
  ```powershell
  python .agent/skills/obsidian-markdown/scripts/run_tracked.py --start [--external "path/to/external/folder"]
  ```
- Run your tools, modifications, and scripts normally.
- **Stop tracking** and write all accumulated changes to `walkthrough.md` at the very end of your verification phase:
  ```powershell
  python .agent/skills/obsidian-markdown/scripts/run_tracked.py --stop
  ```
- This ensures all local line-level changes and external file modifications are tracked and registered exactly once in the feed.
