---
type: sovereign_moc
researcher_name: ""
cssclasses:
  - home-moc
---
# 🛡️ Cybersecurity Command Center


> [!multi-column]
>
> > ### ⚡ Quick Capture
> > ```meta-bind-button
> > style: primary
> > label: "📓 Daily Journal"
> > action:
> >   type: command
> >   command: daily-notes
> > ```
> > ```meta-bind-button
> > style: primary
> > label: "🎯 New Engagement"
> > action:
> >   type: runTemplaterFile
> >   templateFile: "090 System/000 Templates/New Engagement Script.md"
> > ```
> > ```meta-bind-button
> > style: primary
> > label: "🔬 New Research"
> > action:
> >   type: runTemplaterFile
> >   templateFile: "090 System/000 Templates/New Topic Research Script.md"
> > ```
> > ```meta-bind-button
> > style: primary
> > label: "🦠 Malware Analysis"
> > action:
> >   type: runTemplaterFile
> >   templateFile: "090 System/000 Templates/New Malware Analysis Script.md"
> > ```
> >
> > > [!caption] Quick Creation
> > > ```meta-bind-button
> > > style: default
> > > label: "🚩 New CTF Challenge"
> > > action:
> > >   type: runTemplaterFile
> > >   templateFile: "090 System/000 Templates/New CTF Script.md"
> > > ```
> > > ```meta-bind-button
> > > style: default
> > > label: "🚨 New DFIR Case"
> > > action:
> > >   type: runTemplaterFile
> > >   templateFile: "090 System/000 Templates/New DFIR Case Script.md"
> > > ```
> > > ```meta-bind-button
> > > style: default
> > > label: "🖥️ New Lab Machine"
> > > action:
> > >   type: runTemplaterFile
> > >   templateFile: "090 System/000 Templates/New Lab Machine Script.md"
> > > ```
> > > ```meta-bind-button
> > > style: default
> > > label: "🐛 New CVE Note"
> > > action:
> > >   type: runTemplaterFile
> > >   templateFile: "090 System/000 Templates/New CVE Script.md"
> > > ```
> >
> > > ### 🗺️ Navigation
> > > - **Core Operations**
> > >   - [[010 Engagements|🎯 Engagements]]
> > >   - [[080 DFIR|🚨 DFIR Cases]]
> > >   - [[070 Reporting|📄 Reporting]]
> > > - **Research & Intelligence**
> > >   - [[012 Vuln Research|🔍 Vuln Research]]
> > >   - [[013 Topic Research|🔬 Topic Research]]
> > >   - [[020 Threat Intel|📡 Threat Intel]]
> > >   - [[021 Malware Analysis|🦠 Malware Analysis]]
> > > - **Knowledge & Reference**
> > >   - [[040 Knowledge Base|🧠 MITRE KB]]
> > >   - [[030 Tools|🔧 Tool Database]]
> > >   - [[050 References|📚 Reference Library]]
> > > - **Training & Labs**
> > >   - [[011 CTF|🚩 CTF Writeups]]
> > >   - [[060 Labs|🖥️ Practice Labs]]

---

## 🎯 Active Engagements

```dataview
TABLE engagement_type AS "Type", end_date AS "Ends", cvss_critical AS "Crit", cvss_high AS "High", cvss_medium AS "Med", status AS "Status"
FROM "010 Engagements/Active"
WHERE type = "engagement_moc" AND status = "active"
SORT end_date ASC
```

---

## 🔭 Active Research

```dataview
TABLE status AS "Status", started AS "Started", last_updated AS "Updated"
FROM "013 Topic Research"
WHERE type = "topic_research_moc" AND status = "active"
SORT last_updated DESC
```

---

## 🔴 Recent Findings

```dataview
TABLE severity AS "Severity", engagement AS "Engagement", affected_component AS "Component", status AS "Status"
FROM "010 Engagements"
WHERE type = "finding"
SORT date_found DESC
LIMIT 10
```

---

## 🚩 Open CTF Challenges

```dataview
TABLE ctf AS "CTF", category AS "Category", difficulty AS "Difficulty", points AS "Points"
FROM "011 CTF/Active"
WHERE type = "ctf_challenge" AND solved = false
SORT points DESC
```

---

## 🖥️ Lab Queue

```dataview
TABLE platform AS "Platform", os AS "OS", difficulty AS "Difficulty", status AS "Status"
FROM "060 Labs"
WHERE type = "lab_machine" AND status = "in-progress"
SORT difficulty ASC
```

---

## 🚨 Open DFIR Cases

```dataview
TABLE description AS "Description", severity AS "Severity", date_opened AS "Opened", status AS "Status"
FROM "080 DFIR/Cases"
WHERE type = "dfir_case" AND status = "open"
SORT date_opened DESC
```

---

## 📡 Recent Threat Intel

```dataview
LIST
FROM "020 Threat Intel"
SORT file.mtime DESC
LIMIT 8
```

---

## 📋 Today's Tasks

```tasks
not done
due today
```
