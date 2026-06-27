---
type: master_moc
links: "[[000 Home MOC]]"
---
# 🎯 Engagements Command Center

## 📊 Engagements Dashboard
This view is live-synced with your engagement folders. Changing a status here updates the file automatically.

![[Engagements Dashboard.base]]

---

> [!multi-column]
>
> > ### ➕ Quick Actions
> > *Runs the automation script to create folders, templates, and the MOC.*
> > ```meta-bind-button
> > style: primary
> > label: "Create New Engagement"
> > class: btn-project
> > action:
> >   type: runTemplaterFile
> >   templateFile: "090 System/000 Templates/New Engagement Script.md"
> > ```
> > ### 🚦 Vault Status
> > - **Inbox:** [[011 Resource Inbox]]
> > - **Knowledge Base:** [[000 Knowledge Base MOC]]
> > - **Active Engagements:** (View the tabs below)
