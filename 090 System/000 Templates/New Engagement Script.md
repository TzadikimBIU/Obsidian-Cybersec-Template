<%*
// ──────────────────────────────────────────────
// New Engagement Script
// Creates: 010 Engagements/Active/<ClientName>/ with full subfolder structure + MOC
// ──────────────────────────────────────────────

const clientName = await tp.system.prompt("Client / Target Name");
if (!clientName) return;

const engagementType = await tp.system.suggester(
  ["🌐 External Pentest", "🏠 Internal Pentest", "🔴 Red Team", "💰 Bug Bounty", "🌐 Web App", "📱 Mobile App"],
  ["external_pentest", "internal_pentest", "red_team", "bounty", "web_app", "mobile_app"]
);
if (!engagementType) return;

const endDate = await tp.system.prompt("End Date (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD", 30));
if (!endDate) return;

const scopeInput = await tp.system.prompt("Scope (comma separated: domains, IPs, CIDRs)", "");
const scopeItems = scopeInput ? scopeInput.split(",").map(s => `  - "${s.trim()}"`) : [];
const scopeYaml = scopeItems.length > 0 ? `\n${scopeItems.join("\n")}` : " []";

const isActive = await tp.system.suggester(["Active", "Archive", "Bounty"], ["Active", "Archive", "Bounty"]);
const rootPath = `010 Engagements/${isActive}/${clientName}`;

// Create folder structure
const subFolders = ["Recon", "Scans", "Findings", "Exploitation", "Post-Exploitation", "Evidence", "Report"];
if (!app.vault.getAbstractFileByPath(rootPath)) {
  await app.vault.createFolder(rootPath);
  for (const sub of subFolders) {
    await app.vault.createFolder(`${rootPath}/${sub}`);
  }
}

// Read and fill template
const templateFile = app.vault.getAbstractFileByPath("090 System/000 Templates/Engagement MOC Template.md");
if (!templateFile) { new Notice("Engagement MOC Template not found!"); return; }
let content = await app.vault.read(templateFile);

content = content.replace(/{{title}}/g, clientName);
content = content.replace(/{{date}}/g, tp.date.now("YYYY-MM-DD"));

// Inject YAML fields manually
content = content.replace('scope: []', `scope:${scopeYaml}`);
content = content.replace('end_date: ""', `end_date: "${endDate}"`);
content = content.replace('engagement_type: external_pentest', `engagement_type: ${engagementType}`);

const mocPath = `${rootPath}/${clientName} MOC.md`;
await app.vault.create(mocPath, content);

const newFile = app.vault.getAbstractFileByPath(mocPath);
await app.workspace.getLeaf().openFile(newFile);

new Notice(`✅ Engagement "${clientName}" initialized.`);
%>
