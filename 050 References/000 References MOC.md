---
type: master_moc
links: "[[000 Home MOC]]"
---
# 📚 Reference Library

CVEs, academic security papers, advisories, and books.

## 🐛 CVEs
```dataview
TABLE cvss AS "CVSS", product AS "Product", exploit_available AS "Exploit?", summary AS "Summary"
FROM "050 References/CVEs"
WHERE type = "cve"
SORT file.name DESC
```

---

## 📄 Academic Papers & Advisories
```dataview
LIST FROM "050 References"
WHERE type != "cve" AND type != "master_moc"
SORT file.name ASC
```
