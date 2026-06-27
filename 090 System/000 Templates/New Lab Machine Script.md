<%*
// ──────────────────────────────────────────────
// New Lab Machine Script
// Creates a machine note in 060 Labs/<Platform>/Active/
// ──────────────────────────────────────────────

const platform = await tp.system.suggester(
  ["🟢 HackTheBox", "🔵 TryHackMe", "🟡 VulnHub", "🏠 Home Lab", "🎓 CRTE/CRTO/OSCP"],
  ["HTB", "THM", "VulnHub", "Home Lab", "CRTE-CRTO-OSCP"]
);
if (!platform) return;

const machineName = await tp.system.prompt("Machine / Box Name", "");
if (!machineName) return;

const os = await tp.system.suggester(
  ["Linux", "Windows", "FreeBSD", "Other"],
  ["linux", "windows", "freebsd", "other"]
);
const difficulty = await tp.system.suggester(
  ["Easy", "Medium", "Hard", "Insane"],
  ["easy", "medium", "hard", "insane"]
);
const ip = await tp.system.prompt("Target IP", "10.10.10.");

const targetFolder = platform === "HTB" ? `060 Labs/HTB/Active` : `060 Labs/${platform}`;
if (!app.vault.getAbstractFileByPath(targetFolder)) {
  await app.vault.createFolder(targetFolder);
}

const templateFile = app.vault.getAbstractFileByPath("090 System/000 Templates/Lab Machine Template.md");
if (!templateFile) { new Notice("Lab Machine Template not found!"); return; }
let content = await app.vault.read(templateFile);

content = content.replace(/{{title}}/g, machineName);
content = content.replace(/{{date}}/g, tp.date.now("YYYY-MM-DD"));
content = content.replace('platform: hackthebox', `platform: ${platform.toLowerCase().replace(/\//g, "-")}`);
content = content.replace('os: linux', `os: ${os}`);
content = content.replace('difficulty: medium', `difficulty: ${difficulty}`);
content = content.replace('ip: ""', `ip: "${ip}"`);

const finalPath = `${targetFolder}/${machineName}.md`;
await app.vault.create(finalPath, content);
const newFile = app.vault.getAbstractFileByPath(finalPath);
await app.workspace.getLeaf().openFile(newFile);
new Notice(`✅ Machine "${machineName}" created.`);
%>
