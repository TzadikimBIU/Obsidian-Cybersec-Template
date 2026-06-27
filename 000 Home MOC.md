---
type: sovereign_moc
researcher_name: ""
cssclasses:
  - home-moc
---
# 🛡️ Cybersecurity Research Command Center

---

### ⚡ Quick Actions

```meta-bind-button
style: primary
label: "🎯 New Engagement"
class: btn-project
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/New Engagement Script.md"
```

```meta-bind-button
style: primary
label: "🔴 New Finding"
class: btn-homework
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/New Finding Script.md"
```

```meta-bind-button
style: primary
label: "🦠 New Malware Analysis"
class: btn-daily
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/New Malware Analysis Script.md"
```

```meta-bind-button
style: primary
label: "🔭 New Topic Research"
class: btn-idea
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/New Topic Research Script.md"
```

```meta-bind-button
style: primary
label: "🚩 New CTF Challenge"
class: btn-course
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/New CTF Script.md"
```

```meta-bind-button
style: primary
label: "🚨 New DFIR Case"
class: btn-homework
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/New DFIR Case Script.md"
```

```meta-bind-button
style: primary
label: "📅 Daily Log"
class: btn-daily
action:
  type: command
  command: daily-notes
```

---

### 🗺️ Navigation

- [[010 Engagements/Active|🎯 Active Engagements]]
- [[011 CTF|🚩 CTF]]
- [[012 Vuln Research|🔬 Vuln Research]]
- [[013 Topic Research|🔭 Topic Research]]
- [[020 Threat Intel|📡 Threat Intel]]
- [[021 Malware Analysis|🦠 Malware Analysis]]
- [[040 Knowledge Base|📚 Knowledge Base]]
- [[080 DFIR|🚨 DFIR]]

---

## 🎯 Active Engagements

```dataview
TABLE engagement_type AS "Type", end_date AS "Ends", cvss_critical AS "Crit", cvss_high AS "High", cvss_medium AS "Med", status AS "Status"
FROM "010 Engagements/Active"
WHERE type = "engagement_moc" AND status = "active"
SORT end_date ASC
```

---

## 🔭 Active Research

```dataview
TABLE status AS "Status", started AS "Started", last_updated AS "Updated"
FROM "013 Topic Research"
WHERE type = "topic_research_moc" AND status = "active"
SORT last_updated DESC
```

---

## 🔴 Recent Findings

```dataview
TABLE severity AS "Severity", engagement AS "Engagement", affected_component AS "Component", status AS "Status"
FROM "010 Engagements"
WHERE type = "finding"
SORT date_found DESC
LIMIT 10
```

---

## 🚩 Open CTF Challenges

```dataview
TABLE ctf AS "CTF", category AS "Category", difficulty AS "Difficulty", points AS "Points"
FROM "011 CTF/Active"
WHERE type = "ctf_challenge" AND solved = false
SORT points DESC
```

---

## 🖥️ Lab Queue

```dataview
TABLE platform AS "Platform", os AS "OS", difficulty AS "Difficulty", status AS "Status"
FROM "060 Labs"
WHERE type = "lab_machine" AND status = "in-progress"
SORT difficulty ASC
```

---

## 🚨 Open DFIR Cases

```dataview
TABLE description AS "Description", severity AS "Severity", date_opened AS "Opened", status AS "Status"
FROM "080 DFIR/Cases"
WHERE type = "dfir_case" AND status = "open"
SORT date_opened DESC
```

---

## 📡 Recent Threat Intel

```dataview
LIST
FROM "020 Threat Intel"
SORT file.mtime DESC
LIMIT 8
```

---

## 📋 Today's Tasks

```tasks
not done
due today
```
