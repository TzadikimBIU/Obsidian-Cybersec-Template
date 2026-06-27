<%*
// ──────────────────────────────────────────────
// Generate Report Script
// Collects all findings for an engagement and renders a structured pentest report.
// User chooses: Outline (skeleton) or Full (complete rendered markdown).
// ──────────────────────────────────────────────

// 1. Determine engagement
const activeFile = tp.config.active_file;
let engagementName = "";
let engagementPath = "";

if (activeFile) {
  const cache = app.metadataCache.getFileCache(activeFile);
  if (cache?.frontmatter?.type === "engagement_moc") {
    engagementName = activeFile.parent.name;
    engagementPath = activeFile.parent.path;
  }
}

if (!engagementName) {
  const activeFolder = app.vault.getAbstractFileByPath("010 Engagements/Active");
  const engagements = (activeFolder?.children || []).filter(c => c.children).map(c => c.name);
  engagementName = await tp.system.suggester(engagements, engagements);
  if (!engagementName) return;
  engagementPath = `010 Engagements/Active/${engagementName}`;
}

// 2. Choose report type
const reportType = await tp.system.suggester(
  ["📋 Outline (Skeleton)", "📄 Full Report (Complete Markdown)"],
  ["outline", "full"]
);
if (!reportType) return;

// 3. Collect findings
const findingsPath = `${engagementPath}/Findings`;
const findingsFolder = app.vault.getAbstractFileByPath(findingsPath);
const findings = (findingsFolder?.children || []).filter(f => f.extension === "md");

// Sort by severity
const severityOrder = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };
const findingsData = [];
for (const f of findings) {
  const cache = app.metadataCache.getFileCache(f);
  const fm = cache?.frontmatter || {};
  findingsData.push({
    title: fm.title || f.basename,
    severity: fm.severity || "info",
    cvss: fm.cvss || 0,
    cwe: fm.cwe || "",
    component: fm.affected_component || "",
    status: fm.status || "draft",
    path: f.path
  });
}
findingsData.sort((a, b) => (severityOrder[a.severity] ?? 5) - (severityOrder[b.severity] ?? 5));

const today = tp.date.now("YYYY-MM-DD");
const critical = findingsData.filter(f => f.severity === "critical").length;
const high = findingsData.filter(f => f.severity === "high").length;
const medium = findingsData.filter(f => f.severity === "medium").length;
const low = findingsData.filter(f => f.severity === "low").length;

// 4. Build report content
let report = `---
type: pentest_report
engagement: "${engagementName}"
report_date: ${today}
report_type: ${reportType}
tags:
  - report
---
# Penetration Test Report
## ${engagementName}

**Report Date:** ${today}  
**Report Type:** ${reportType === "outline" ? "Outline / Skeleton" : "Full Technical Report"}

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | ${critical} |
| 🟠 High | ${high} |
| 🟡 Medium | ${medium} |
| 🔵 Low | ${low} |

`;

if (reportType === "outline") {
  report += `> **Instructions:** This is a skeleton report. Fill in each section with your engagement narrative and copy finding details from the individual finding notes.\n\n`;
  report += `### Findings Summary\n\n`;
  report += `| ID | Title | Severity | Component | Status |\n|---|---|---|---|---|\n`;
  for (const f of findingsData) {
    report += `| | ${f.title} | ${f.severity} | ${f.component} | ${f.status} |\n`;
  }
  report += `\n---\n\n## Methodology\n\n*Describe the testing methodology used.*\n\n---\n\n## Detailed Findings\n\n`;
  for (const f of findingsData) {
    report += `### ${f.title}\n\n**Severity:** ${f.severity} | **CVSS:** ${f.cvss} | **CWE:** ${f.cwe}\n\n> Copy from [[${f.path}]]\n\n---\n\n`;
  }
  report += `## Recommendations Summary\n\n*Prioritized list of remediation actions.*\n\n`;

} else {
  // Full report — embed content from each finding note
  report += `### Findings Summary\n\n`;
  report += `| ID | Title | Severity | CVSS | Component |\n|---|---|---|---|---|\n`;
  for (const f of findingsData) {
    report += `| | ${f.title} | ${f.severity} | ${f.cvss} | ${f.component} |\n`;
  }
  report += `\n---\n\n## Methodology\n\n*Describe the engagement scope, phases, and approach.*\n\n---\n\n## Detailed Findings\n\n`;
  for (const f of findingsData) {
    const fFile = app.vault.getAbstractFileByPath(f.path);
    if (fFile) {
      let fContent = await app.vault.read(fFile);
      // Strip frontmatter
      fContent = fContent.replace(/^---[\s\S]*?---\n/, "");
      report += fContent + "\n\n---\n\n";
    }
  }
  report += `## Recommendations Summary\n\n*See individual findings for detailed recommendations.*\n\n`;
}

// 5. Create report file
const reportFolder = `${engagementPath}/Report`;
if (!app.vault.getAbstractFileByPath(reportFolder)) {
  await app.vault.createFolder(reportFolder);
}

const reportPath = `${reportFolder}/${engagementName} Report ${today}.md`;
await app.vault.create(reportPath, report);
const newFile = app.vault.getAbstractFileByPath(reportPath);
await app.workspace.getLeaf().openFile(newFile);
new Notice(`✅ ${reportType === "outline" ? "Outline" : "Full"} report generated: ${findings.length} finding(s).`);
%>
