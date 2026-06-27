---
type: engagement_moc
client: "{{title}}"
scope: []
start_date: {{date}}
end_date: ""
status: active
engagement_type: external_pentest
cvss_critical: 0
cvss_high: 0
cvss_medium: 0
cvss_low: 0
cvss_info: 0
tags:
  - engagement
---
# 🎯 {{title}} — Engagement

**Type:** `=this.engagement_type` | **Status:** `=this.status`  
**Period:** `=this.start_date` → `=this.end_date`

---

## ⚡ Quick Actions

```meta-bind-button
style: primary
label: "🔴 New Finding"
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/New Finding Script.md"
```

```meta-bind-button
style: default
label: "🗺️ New Recon Note"
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/Smart Sec Note Creator.md"
```

```meta-bind-button
style: default
label: "📄 Generate Report"
action:
  type: runTemplaterFile
  templateFile: "090 System/000 Templates/Generate Report Script.md"
```

---

## 🗂️ Scope

```
# Add targets here — IPs, domains, CIDR ranges
```

---

## 🔴 Findings

```dataview
TABLE severity AS "Severity", affected_component AS "Component", status AS "Status"
FROM ""
WHERE type = "finding" AND contains(string(engagement), this.file.name)
SORT choice(severity = "critical", 0, choice(severity = "high", 1, choice(severity = "medium", 2, choice(severity = "low", 3, 4)))) ASC
```

---

## 📋 Open Tasks

```tasks
not done
path includes {{title}}
```

---

## 📅 Timeline

| Date | Event |
|------|-------|
| `=this.start_date` | Engagement started |
