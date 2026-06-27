<%*
// ──────────────────────────────────────────────
// New CTF Script
// Creates a challenge note in 011 CTF/Active/<CTF Name>/<Category>/
// ──────────────────────────────────────────────

const ctfName = await tp.system.prompt("CTF Name (e.g. PicoCTF 2026)", "");
if (!ctfName) return;

const category = await tp.system.suggester(
  ["🌐 Web", "💥 Pwn", "🔐 Crypto", "🔍 Forensics", "⚙️ Reversing", "🌀 Misc", "👁️ OSINT"],
  ["Web", "Pwn", "Crypto", "Forensics", "Reversing", "Misc", "OSINT"]
);
if (!category) return;

const challengeName = await tp.system.prompt("Challenge Name", "");
if (!challengeName) return;

const points = await tp.system.prompt("Points", "0");
const difficulty = await tp.system.suggester(
  ["Easy", "Medium", "Hard", "Insane"],
  ["easy", "medium", "hard", "insane"]
);

const targetFolder = `011 CTF/Active/${ctfName}/${category}`;
if (!app.vault.getAbstractFileByPath(targetFolder)) {
  await app.vault.createFolder(targetFolder);
}

const templateFile = app.vault.getAbstractFileByPath("090 System/000 Templates/CTF Challenge Template.md");
if (!templateFile) { new Notice("CTF Challenge Template not found!"); return; }
let content = await app.vault.read(templateFile);
content = content.replace(/{{title}}/g, challengeName);
content = content.replace(/{{ctf}}/g, ctfName);
content = content.replace(/{{flag}}/g, "");
content = content.replace(/{{date}}/g, tp.date.now("YYYY-MM-DD"));
content = content.replace("category: web", `category: ${category.toLowerCase()}`);
content = content.replace("difficulty: medium", `difficulty: ${difficulty}`);
content = content.replace("points: 0", `points: ${points}`);

const finalPath = `${targetFolder}/${challengeName}.md`;
await app.vault.create(finalPath, content);
const newFile = app.vault.getAbstractFileByPath(finalPath);
await app.workspace.getLeaf().openFile(newFile);
new Notice(`✅ CTF challenge "${challengeName}" created.`);
%>
