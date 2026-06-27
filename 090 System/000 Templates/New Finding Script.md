<%*
// ──────────────────────────────────────────────
// New Finding Script
// Auto-numbers FIND-NNN, creates finding note inside the active engagement folder
// ──────────────────────────────────────────────

// 1. Determine engagement from current file context or prompt
const activeFile = tp.config.active_file;
let engagementPath = "";
let engagementName = "";

if (activeFile) {
  const cache = app.metadataCache.getFileCache(activeFile);
  if (cache?.frontmatter?.type === "engagement_moc") {
    engagementPath = activeFile.parent.path;
    engagementName = activeFile.parent.name;
  }
}

if (!engagementPath) {
  // Let user pick from active engagements
  const activeFolder = app.vault.getAbstractFileByPath("010 Engagements/Active");
  if (!activeFolder || !activeFolder.children) { new Notice("No active engagements found."); return; }
  const engagements = activeFolder.children.filter(c => c.children).map(c => c.name);
  engagementName = await tp.system.suggester(engagements, engagements);
  if (!engagementName) return;
  engagementPath = `010 Engagements/Active/${engagementName}`;
}

// 2. Auto-number: count existing findings
const findingsFolder = app.vault.getAbstractFileByPath(`${engagementPath}/Findings`);
let nextNum = 1;
if (findingsFolder && findingsFolder.children) {
  const existing = findingsFolder.children.filter(f => f.name.startsWith("FIND-"));
  nextNum = existing.length + 1;
}
const findingId = `FIND-${String(nextNum).padStart(3, "0")}`;

// 3. Prompt for finding details
const title = await tp.system.prompt("Finding Title", "");
if (!title) return;

const severity = await tp.system.suggester(
  ["🔴 Critical", "🟠 High", "🟡 Medium", "🔵 Low", "ℹ️ Info"],
  ["critical", "high", "medium", "low", "info"]
);
if (!severity) return;

const cwe = await tp.system.prompt("CWE (e.g. CWE-89)", "");
const component = await tp.system.prompt("Affected Component", "");

// 4. Load and fill template
const templateFile = app.vault.getAbstractFileByPath("090 System/000 Templates/Finding Template.md");
if (!templateFile) { new Notice("Finding Template not found!"); return; }
let content = await app.vault.read(templateFile);

content = content.replace(/{{title}}/g, `${findingId} ${title}`);
content = content.replace(/{{date}}/g, tp.date.now("YYYY-MM-DD"));
content = content.replace('severity: high', `severity: ${severity}`);
content = content.replace('cwe: ""', `cwe: "${cwe}"`);
content = content.replace('affected_component: ""', `affected_component: "${component}"`);
content = content.replace('engagement: "[[]]"', `engagement: "[[${engagementName} MOC]]"`);

// 5. Create and open
if (!app.vault.getAbstractFileByPath(`${engagementPath}/Findings`)) {
  await app.vault.createFolder(`${engagementPath}/Findings`);
}
const finalPath = `${engagementPath}/Findings/${findingId} ${title}.md`;
await app.vault.create(finalPath, content);
const newFile = app.vault.getAbstractFileByPath(finalPath);
await app.workspace.getLeaf().openFile(newFile);

new Notice(`✅ ${findingId} created.`);
%>
