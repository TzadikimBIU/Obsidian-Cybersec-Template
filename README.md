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
| **New CVE** | CVE reference note in `050 References/CVEs/` |
| **New Lab Machine** | Machine note in the correct lab platform folder |
| **Generate Report** | Collects all engagement findings; choose **Outline** or **Full Report** |
| **Smart Sec Note Creator** | Context-aware note creator — run from any MOC |

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
