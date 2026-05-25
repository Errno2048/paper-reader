# paper-reader

Fully automated multi-agent paper reading for Claude Code. Three agents (Reviewer, Reader, Questioner) collaborate to produce a comprehensive, reproducibility-focused report from an academic paper (PDF or Markdown).

## How It Works

1. **Reviewer** — Reads the full paper, creates a domain-specific report template with guiding questions. Later arbitrates inconsistencies between reports.
2. **Reader** — Reads the full paper deeply, fills the template with detailed content, and answers the Questioner's questions.
3. **Questioner** — Reads only the abstract and the Reader's report. Asks targeted questions about reproducibility gaps.

The key insight: the Questioner's limited access forces it to catch gaps the Reader might overlook due to over-familiarity with the text.

## Installation

**Option 1: Marketplace (recommended)**

```bash
/plugin marketplace add https://github.com/Errno2048/paper-reader.git
/plugin install paper-skills@paper-reader-skills
```

**Option 2: Manual clone**

```bash
git clone https://github.com/Errno2048/paper-reader.git ~/.claude/skills/paper-reader
```

## Requirements

- Python 3.8+
- PyMuPDF (`pip install pymupdf`) — required for PDF extraction
- pymupdf4llm (`pip install pymupdf4llm`) — optional, for higher quality Markdown extraction

## Usage

In Claude Code:

```
/paper-reader
```

Provide a PDF file path or a directory containing `paper.md` when prompted.

## Output

| File | Description |
|------|-------------|
| `template_extended.md` | Domain-specific reading template |
| `reader_report.md` | Comprehensive report from full paper reading |
| `questioner_report.md` | Independent reproducibility assessment |
| `final_report.md` | Arbitrated final report |
| `summary_report.md` | Concise 1-page summary |

## Project Structure

```
paper-reader/
├── README.md
├── .gitignore
├── .claude-plugin/
│   └── marketplace.json              # Marketplace registration
└── skills/
    └── paper-reader/
        ├── SKILL.md                  # Skill definition (YAML frontmatter + body)
        ├── agents/
        │   ├── reviewer_agent.md     # Reviewer agent instructions
        │   ├── reader_agent.md       # Reader agent instructions
        │   └── questioner_agent.md   # Questioner agent instructions
        ├── templates/
        │   └── generic_cs_template.md # Base report template (13 sections)
        ├── references/
        │   └── reproducibility_checklist.md  # Checklist for systematic gap assessment
        └── scripts/
            └── extract_paper.py      # PDF → Markdown extraction with fallback
```

## License

MIT
