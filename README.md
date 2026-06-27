# 🛡️ Obsidian Cybersecurity Research Vault Template

A structured Obsidian vault template for **cybersecurity researchers** spanning red team, blue team, malware analysis, vulnerability research, CTF, and DFIR. Built on a PARA/Johnny Decimal hybrid system with deep automation via Templater, Dataview, and MetaBind.

---

## 🚀 Getting Started

### 1. Clone the Vault

```bash
git clone https://github.com/Tzadikimctf/Obsidian-Cybersec-Template.git
```

### 2. Open in Obsidian

1. Open Obsidian → **Open folder as vault**
2. Select the cloned `Obsidian-Cybersec-Template` folder

### 3. Install & Enable Plugins

All plugin **configurations** are pre-bundled in `.obsidian/`. You must install the plugin binaries through Obsidian's Community Plugins browser:

1. **Settings** → **Community Plugins** → **Browse**
2. Install and enable all plugins in the Required Plugins table below

### 4. Configure Lotus for Code Execution

1. **Settings** → **Lotus** → Enable **Local Execution** (acknowledge the risk modal)
2. Under **Execution Groups**, configure the pre-defined groups:
   - `docker_pentest` — Kali Docker container (requires Docker Desktop)
   - `docker_reversing` — Reversing container with radare2
   - `wsl_kali` — WSL Kali distribution
   - `ssh_vps` — Remote SSH target (set your host in the config)
3. Set Python, Shell, and C executable paths under **Built-in Runtimes**

### 5. Open Your Dashboard

Open **`000 Home MOC.md`** — your research command center with live engagement dashboards, finding trackers, and quick-action buttons.

---

## 📂 Vault Structure

```
000 Home MOC.md              ← Research command center
001 Daily Logs/              ← Session journals and daily logs
010 Engagements/             ← Pentests, red team ops, bug bounty
011 CTF/                     ← CTF challenges (active + technique reference archive)
012 Vuln Research/           ← Target-specific vulnerability research
013 Topic Research/          ← Self-directed domain deep dives (anti-RE, kernel, etc.)
020 Threat Intel/            ← APT groups, campaigns, IOCs
021 Malware Analysis/        ← Sample-specific reverse engineering sessions
030 Tools/                   ← Tool docs, one-liners, configs
040 Knowledge Base/          ← Permanent MITRE-mapped technique notes
050 References/              ← CVEs, papers, advisories, books
060 Labs/                    ← HTB, THM, VulnHub, home lab notes
070 Reporting/               ← Report templates and deliverables
080 DFIR/                    ← Incident response cases and playbooks
090 System/                  ← Automation scripts, templates, attachments
```

---

## 🔌 Required Plugins

| Plugin | Purpose |
|--------|---------|
| **Templater** | All automation scripts and note generation |
| **Dataview** | Live dashboards — finding tables, engagement trackers |
| **Meta Bind** | Quick-action buttons on the Home MOC |
| **Obsidian Tasks** | Cross-vault task tracking |
| **Lotus** | Live code block execution in notes (PoC testing, recon, analysis) |
| **Obsidian Git** | Auto-commit notes for evidence integrity |
| **Excalidraw** | Network diagrams, attack path visualization |
| **Kanban** | Engagement status boards |
| **Calendar** | Daily log navigation |
| **Notebook Navigator** | Sequential navigation through engagement/research notes |

---

## ⚡ Automation Scripts

All scripts live in `090 System/000 Templates/` and are triggered via **MetaBind buttons** on `000 Home MOC.md` or via Templater's hotkey.

| Script | What it creates |
|--------|-----------------|
| **New Engagement** | `010 Engagements/Active/<Client>/` with full subfolder structure + MOC |
| **New Finding** | Auto-numbered `FIND-NNN <title>.md` inside the active engagement |
| **New Topic Research** | `013 Topic Research/<Topic>/` with MOC and Experiments folder |
| **New Malware Analysis** | `021 Malware Analysis/<Name>/` with full analysis folder |
| **New CTF Challenge** | Challenge note routed to correct CTF/category folder |
| **New DFIR Case** | Auto-numbered `INC-NNN` case with MOC, Timeline, and IOC notes |
| **New Lab Machine** | Machine note in the correct lab platform folder |
| **New CVE** | CVE reference note in `050 References/CVEs/` |
| **Generate Report** | Collects all engagement findings; choose **Outline** or **Full Report** |
| **Smart Sec Note Creator** | Context-aware note creator — run from any MOC |

### 🎛️ MetaBind Control Panel Buttons

The **`000 Home MOC.md`** command center contains quick-action buttons powered by **MetaBind**:
*   **📓 Daily Journal**: Opens or creates the Daily Log note for today (`001 Daily Logs/YYYY-MM-DD.md`) using Obsidian's daily notes command.
*   **🎯 New Engagement**: Triggers the `New Engagement Script.md` to scaffold a client folder and create an Engagement MOC.
*   **🔬 New Research**: Triggers the `New Topic Research Script.md` to begin a self-directed topic research folder structure.
*   **🦠 Malware Analysis**: Triggers the `New Malware Analysis Script.md` to reverse engineer a specific sample.
*   **🚩 New CTF Challenge**: Triggers the `New CTF Script.md` to write a CTF writeup note.
*   **🚨 New DFIR Case**: Triggers the `New DFIR Case Script.md` to scaffold an incident case folder with Timeline and IOC trackers.
*   **🖥️ New Lab Machine**: Triggers the `New Lab Machine Script.md` to write a walkthrough for HTB/THM machines.
*   **🐛 New CVE Note**: Triggers the `New CVE Script.md` to create a reference note for a vulnerability.

### 📋 Templater Notes & Templates

The vault comes with pre-configured templates under `090 System/000 Templates/` to standardize metadata schemas for Dataview dashboards:
*   **`Daily Log Template.md`**: For logging objectives, session diaries, commands run, findings, and next-day planning.
*   **`Engagement MOC Template.md`**: Standardizes client dashboards, detailing CVSS aggregations, scope blocks, active findings, and tasks.
*   **`Finding Template.md`**: Used for recording vulnerability findings with severity ratings, CVSS score/vector, CVE/CWE, affected components, steps to reproduce (with Lotus code blocks), evidence, and recommendations.
*   **`Topic Research MOC Template.md`**: Tracks key research questions, literature reading status, progress journals, and experiments.
*   **`Research Experiment Template.md`**: For writing down isolated tests or PoC code within a topic research area.
*   **`Malware Analysis Template.md`**: For tracking file hashes (MD5/SHA256), static reversing metadata (strings, imports/exports), dynamic behavior logs, and MITRE ATT&CK mapping.
*   **`CTF Challenge Template.md`**: Details solved CTF challenges, flags, walkthroughs, and maps them to real-world techniques.
*   **`DFIR Playbook Template.md`**: Outlines incident response phase checklists (Triage, Containment, Investigation, Eradication, Recovery, Lessons Learned).
*   **`Lab Machine Template.md`**: Structures lab machine writeups (Nmap port scans, footholds, privilege escalation, user/root flags).
*   **`CVE Template.md`**: Holds technical details, exploit availability, PoCs, and remediations for specific CVE vulnerability entries.
*   **`Technique Note Template.md`**: Holds permanent MITRE ATT&CK technique descriptions, Sigma/YARA rules, and threat actor maps.
*   **`Tool Note Template.md`**: Configures cheat sheets, installation steps, and CLI one-liners for security tools.

---

## 🔬 Lotus Execution Groups

Pre-configured execution groups for running code inside notes:

| Group | Runtime | Purpose |
|-------|---------|---------|
| `native` | Host machine | Default — local Python, shell |
| `docker_pentest` | Kali Docker | Isolated PoC testing |
| `docker_reversing` | radare2 Docker | Binary analysis experiments |
| `wsl_kali` | WSL Kali | Linux tools on Windows host |
| `ssh_vps` | Remote SSH | Commands on remote VPS |

To add your own SSH VPS target, edit `.obsidian/plugins/lotus/containers/ssh_vps/config.json`.

---

## 🏗️ Design Philosophy

### Three Research Tiers

| Location | Use for | Becomes |
|----------|---------|---------|
| `013 Topic Research/<Topic>/` | Raw research, experiments, reading | → |
| `021 Malware Analysis/<Sample>/` | Specific sample analysis sessions | → |
| `040 Knowledge Base/<Tactic>/` | Crystallized, permanent technique notes | ✅ |

Ideas flow **013/021 → 040** as they mature. Cross-links keep everything connected.

### The Finding is the Core Unit

Every engagement note resolves to `Finding Template.md`. Findings are:
- Auto-numbered (`FIND-001`, `FIND-002`, ...)
- Severity-tagged (critical/high/medium/low/info)
- Structured for copy-paste into the report generator

### CTF as Technique Reference

CTF challenges include **Real-World Relevance** and **Technique Link** fields that link back to `040 Knowledge Base/` notes and real CVEs. Over time, your solved challenges become a searchable technique reference library.

---

## 🔒 Security & Privacy Notes

> [!CAUTION]
> Lotus executes code blocks directly on your machine (or in configured containers). Never run code blocks from untrusted notes. Use `docker_pentest` or `wsl_kali` groups for isolation when testing potentially dangerous PoC code.

> [!WARNING]
> Before pushing to a public repository, uncomment the client engagement exclusion block in `.gitignore` to ensure client data is never committed:
> ```
> 010 Engagements/Active/
> 010 Engagements/Archive/
> 080 DFIR/Cases/
> ```

---

## 📄 License

MIT — see `LICENSE` file.
