<%*
// ──────────────────────────────────────────────
// New Topic Research Script
// Scaffolds 013 Topic Research/<TopicName>/ with MOC, subfolders, and Papers dir
// ──────────────────────────────────────────────

const topicName = await tp.system.prompt("Research Topic Name (e.g. Anti-Reverse Engineering)");
if (!topicName) return;

const rootPath = `013 Topic Research/${topicName}`;
const subFolders = ["Experiments", "Papers & References"];

if (!app.vault.getAbstractFileByPath(rootPath)) {
  await app.vault.createFolder(rootPath);
  for (const sub of subFolders) {
    await app.vault.createFolder(`${rootPath}/${sub}`);
  }
}

const templateFile = app.vault.getAbstractFileByPath("090 System/000 Templates/Topic Research MOC Template.md");
if (!templateFile) { new Notice("Topic Research MOC Template not found!"); return; }
let content = await app.vault.read(templateFile);
content = content.replace(/{{title}}/g, topicName);
content = content.replace(/{{date}}/g, tp.date.now("YYYY-MM-DD"));

const mocPath = `${rootPath}/${topicName} MOC.md`;
await app.vault.create(mocPath, content);
const newFile = app.vault.getAbstractFileByPath(mocPath);
await app.workspace.getLeaf().openFile(newFile);
new Notice(`✅ Topic Research "${topicName}" initialized.`);
%>
