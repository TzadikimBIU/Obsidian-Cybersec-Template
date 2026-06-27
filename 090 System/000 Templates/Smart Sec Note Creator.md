<%*
// ──────────────────────────────────────────────
// Smart Security Note Creator
// Context-aware note creator: works from Engagement MOC, CTF MOC, or Topic Research MOC
// ──────────────────────────────────────────────

const activeFile = tp.config.active_file;
if (!activeFile) { new Notice("Error: No active file."); return; }

const cache = app.metadataCache.getFileCache(activeFile);
const mocType = cache?.frontmatter?.type;
const parentFolder = activeFile.parent.path;
const parentName = activeFile.parent.name;

let templatePath = "";
let subFolder = "";

if (mocType === "engagement_moc") {
  const choice = await tp.system.suggester(
    ["🗺️ Recon Note", "🔍 Scan Note", "💥 Exploitation Note", "📝 General Note"],
    ["Recon", "Scans", "Exploitation", ""]
  );
  if (choice === null) return;
  subFolder = choice;
  templatePath = "090 System/000 Templates/Engagement Recon Template.md";

} else if (mocType === "topic_research_moc") {
  const choice = await tp.system.suggester(
    ["🧪 Experiment", "📝 Research Note"],
    ["experiment", "note"]
  );
  if (choice === "experiment") {
    templatePath = "090 System/000 Templates/Research Experiment Template.md";
    subFolder = "Experiments";
  } else {
    // Generic note in the topic folder
    subFolder = "";
    templatePath = "";
  }

} else {
  new Notice("Open this from an Engagement MOC or Topic Research MOC.");
  return;
}

const noteName = await tp.system.prompt("Note Name", "");
if (!noteName) return;

const targetFolder = subFolder ? `${parentFolder}/${subFolder}` : parentFolder;
if (subFolder && !app.vault.getAbstractFileByPath(targetFolder)) {
  await app.vault.createFolder(targetFolder);
}

let content = "";
if (templatePath) {
  const templateFile = app.vault.getAbstractFileByPath(templatePath);
  if (templateFile) {
    content = await app.vault.read(templateFile);
    content = content.replace(/{{title}}/g, noteName);
    content = content.replace(/{{date}}/g, tp.date.now("YYYY-MM-DD"));
  }
} else {
  content = `---\ntype: research_note\ntopic: "[[${activeFile.basename}]]"\ndate: ${tp.date.now("YYYY-MM-DD")}\n---\n# ${noteName}\n\n`;
}

const finalPath = `${targetFolder}/${noteName}.md`;
await app.vault.create(finalPath, content);
const newFile = app.vault.getAbstractFileByPath(finalPath);
await app.workspace.getLeaf().openFile(newFile);

setTimeout(() => {
  app.commands.executeCommandById("templater-obsidian:replace-templates-active-file");
}, 100);
%>
