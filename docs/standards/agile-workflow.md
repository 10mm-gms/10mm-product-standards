# Agile-as-Code Standard

This standard provides a "middle ground" between heavy Scrum tools (Jira, Linear) and unmanaged text files. It separates **Management** (Prioritization) from **Definition** (Requirements).

## 1. The Manager View: `BOARD.md`
To avoid learning Markdown syntax for management, we use a single file `planning/BOARD.md` that acts as your Kanban board. You simply move lines up and down.

**Structure:**
*   **Backlog**: Ideas and future work.
*   **Ready**: Specs are defined, ready for dev.
*   **In Progress**: Active work.
*   **Done**: Completed.

**Format (Simple List):**
```markdown
# Board

## In Progress
- [ ] [STORY-101] Login Page (assigned: @me)

## Ready (Prioritized)
- [ ] [STORY-102] Forgot Password Flow
- [ ] [STORY-105] User Profile

## Backlog
- [ ] [EPIC-A] Admin Dashboard
- [ ] Something about email notifications (needs spec)
```
*You treat this file like a drag-and-drop list.*

## 2. The Artifacts: Epics & Stories
Instead of flat folders, we use a hierarchical structure. Every Epic has its own directory.

*   **Epics** (`planning/epics/[EPIC-ID]/epic.md`): High-level goals.
*   **Stories** (`planning/epics/[EPIC-ID]/stories/*.md`): Specific, shippable units that live *inside* the epic folder.

### The AI-Assisted Workflow
1.  **You** add a bullet point to `BOARD.md`: "- [ ] [EPIC-10] User Profile".
2.  **AI (Me)** creates `planning/epics/EPIC-10-user-profile/epic.md`.
3.  **We** add stories under `planning/epics/EPIC-10-user-profile/stories/STORY-11.md`.

## 3. Directory Structure
```text
product_standards/
└── planning/
    ├── BOARD.md
    └── epics/
        └── EPIC-10-user-profile/
            ├── epic.md
            └── stories/
                ├── STORY-11-edit-avatar.md
                └── STORY-12-change-password.md
```

## Why this works?
1.  **Prioritization**: You just reorder lines in `BOARD.md`.
2.  **Context**: AI can read all files easily, unlike a closed SaaS tool.
3.  **Low Friction**: You write bullets; AI writes the complex Markdown.
