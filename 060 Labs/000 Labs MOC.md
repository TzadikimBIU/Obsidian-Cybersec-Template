---
type: master_moc
links: "[[000 Home MOC]]"
---
# 🖥️ Practice Labs

Track your progress on HackTheBox, TryHackMe, VulnHub, and Home Lab networks.

---

## 🎯 Active Lab Targets
```dataview
TABLE platform AS "Platform", os AS "OS", difficulty AS "Difficulty", ip AS "IP Address"
FROM "060 Labs"
WHERE type = "lab_machine" AND status = "in-progress"
SORT difficulty ASC
```

---

## ✅ Rooted / Completed
```dataview
TABLE platform AS "Platform", difficulty AS "Difficulty", user_flag AS "User", root_flag AS "Root"
FROM "060 Labs"
WHERE type = "lab_machine" AND status = "rooted"
SORT file.name ASC
```
