<%*
// ──────────────────────────────────────────────
// New CVE Script
// Creates a CVE reference note in 050 References/CVEs/
// ──────────────────────────────────────────────

const cveId = await tp.system.prompt("CVE ID (e.g. CVE-2024-12345)", "CVE-");
if (!cveId) return;

const product = await tp.system.prompt("Affected Product", "");
const vendor = await tp.system.prompt("Vendor", "");
const cvss = await tp.system.prompt("CVSS Score (0.0–10.0)", "");
const summary = await tp.system.prompt("One-line summary", "");
const exploitAvailable = await tp.system.suggester(["Yes", "No"], ["true", "false"]);

const templateFile = app.vault.getAbstractFileByPath("090 System/000 Templates/CVE Template.md");
if (!templateFile) { new Notice("CVE Template not found!"); return; }
let content = await app.vault.read(templateFile);

content = content.replace(/{{cve_id}}/g, cveId);
content = content.replace(/{{title}}/g, cveId);
content = content.replace(/{{date}}/g, tp.date.now("YYYY-MM-DD"));
content = content.replace('product: ""', `product: "${product}"`);
content = content.replace('vendor: ""', `vendor: "${vendor}"`);
content = content.replace('cvss: 0.0', `cvss: ${cvss || 0}`);
content = content.replace('summary: ""', `summary: "${summary}"`);
content = content.replace('exploit_available: false', `exploit_available: ${exploitAvailable}`);

const targetFolder = "050 References/CVEs";
if (!app.vault.getAbstractFileByPath(targetFolder)) {
  await app.vault.createFolder(targetFolder);
}

const finalPath = `${targetFolder}/${cveId}.md`;
await app.vault.create(finalPath, content);
const newFile = app.vault.getAbstractFileByPath(finalPath);
await app.workspace.getLeaf().openFile(newFile);
new Notice(`✅ ${cveId} reference created.`);
%>
