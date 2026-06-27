<%*
// ──────────────────────────────────────────────
// New DFIR Case Script
// Creates INC-NNN case folder with MOC, Timeline, and IOCs notes
// ──────────────────────────────────────────────

const casesFolder = app.vault.getAbstractFileByPath("080 DFIR/Cases");
let nextNum = 1;
if (casesFolder && casesFolder.children) {
  const existing = casesFolder.children.filter(c => c.name.startsWith("INC-"));
  nextNum = existing.length + 1;
}
const incId = `INC-${String(nextNum).padStart(3, "0")}`;

const description = await tp.system.prompt("Incident Description", "");
if (!description) return;

const severity = await tp.system.suggester(
  ["🔴 Critical", "🟠 High", "🟡 Medium", "🔵 Low"],
  ["critical", "high", "medium", "low"]
);

const caseName = `${incId} ${description}`;
const casePath = `080 DFIR/Cases/${caseName}`;

await app.vault.createFolder(casePath);
await app.vault.createFolder(`${casePath}/Artifacts`);

// Create MOC
const mocContent = `---
type: dfir_case
case_id: "${incId}"
description: "${description}"
severity: ${severity}
date_opened: ${tp.date.now("YYYY-MM-DD")}
date_closed: ""
status: open
tags:
  - dfir
  - incident
---
# 🚨 ${caseName}

**Severity:** \`=this.severity\` | **Status:** \`=this.status\`  
**Opened:** \`=this.date_opened\`

---

## ⚡ Quick Actions

\`\`\`meta-bind-button
style: primary
label: "📋 Open Playbook"
action:
  type: open
  link: "080 DFIR/Playbooks/"
\`\`\`

---

## 📋 Summary

---

## 📅 Timeline

See [[${caseName}/Timeline]]

## 📡 IOCs

See [[${caseName}/IOCs]]
`;

await app.vault.create(`${casePath}/${incId} MOC.md`, mocContent);

// Create Timeline
await app.vault.create(`${casePath}/Timeline.md`, `---
type: dfir_timeline
case: "[[${incId} MOC]]"
---
# Timeline — ${caseName}

| Timestamp | System | Event | Source |
|-----------|--------|-------|--------|
| | | | |
`);

// Create IOCs
await app.vault.create(`${casePath}/IOCs.md`, `---
type: dfir_iocs
case: "[[${incId} MOC]]"
---
# IOCs — ${caseName}

| Type | Value | Confidence | Notes |
|------|-------|------------|-------|
| | | | |
`);

const newFile = app.vault.getAbstractFileByPath(`${casePath}/${incId} MOC.md`);
await app.workspace.getLeaf().openFile(newFile);
new Notice(`✅ DFIR Case ${incId} initialized.`);
%>
