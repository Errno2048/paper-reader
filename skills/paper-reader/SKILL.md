---
name: paper-reader
description: Fully automated multi-agent paper reading. Three agents (Reviewer, Reader, Questioner) collaborate to produce a comprehensive, reproducibility-focused paper report from a PDF or Markdown input.
metadata:
  type: skill
  version: "1.0"
  requires:
    - Python 3.8+
    - PyMuPDF (fitz) — installed by default in most environments
    - pymupdf4llm — optional, for higher quality Markdown extraction
  agent_team: true
allowed-tools: Read, Write, Bash, PowerShell, Glob, Grep, TeamCreate, Agent, SendMessage, TaskCreate, TaskUpdate, AskUserQuestion
---

# Paper Reader — Multi-Agent Paper Reading

## Overview

This skill orchestrates three agents to deeply read and analyze an academic paper:

1. **Reviewer** — reads the full paper first, creates a domain-specific report template (questions only, no answers). Later, compares the Reader's and Questioner's independent reports, arbitrates all inconsistencies by consulting the original paper, and produces the final report.

2. **Reader** — reads the full paper deeply, fills the Reviewer's template with content, and answers the Questioner's questions during the Q&A phase.

3. **Questioner** — reads only the abstract and the Reader's report (not the full paper). Asks targeted questions about what's needed to reproduce the method and results. Produces an independent report.

The key insight: the Questioner's limited access forces it to catch gaps that the Reader (who read everything) might have overlooked due to over-familiarity with the text.

## Input

The user may provide:
- A **PDF file path** → extraction runs automatically
- A **directory path** containing `paper.md` (and optionally `images/`) → extraction is skipped

## Output

All outputs are written to `<paper_dir>/`, where `<paper_dir>` is the directory containing the paper:

| File | Phase | Producer |
|------|-------|----------|
| `paper.md` | Extraction | Script |
| `abstract.md` | Extraction | Orchestrator |
| `template_extended.md` | 0 | Reviewer |
| `reader_report.md` | 1 | Reader |
| `questioner_report.md` | 2 | Questioner |
| `final_report.md` | 3 | Reviewer |
| `summary_report.md` | 3 | Reviewer |

The user receives the path to `final_report.md`.

## Orchestration Flow

Follow these steps in order. Do not skip or reorder.

---

### Step 0: Resolve Input

Ask the user for the paper path if not provided.

```
If the input is a directory:
  If <directory>/paper.md exists → paper_dir = <directory>, skip to Step 2
  Else → error: "Directory does not contain paper.md"

If the input is a PDF file:
  paper_dir = <pdf_directory>/<pdf_basename_without_extension>/
  Proceed to Step 1

If no input provided:
  AskUserQuestion: "Please provide the path to the paper (PDF file or directory with paper.md)"
```

---

### Step 1: Extract PDF to Markdown

Run the extraction script:

```powershell
conda activate base
python "$env:SKILL_DIR\scripts\extract_paper.py" "<pdf_path>" --output-dir "<paper_dir>"
```

Parse the stdout output:
- `OK:pymupdf4llm:...` → extraction succeeded with best quality, proceed to Step 2
- `OK:pymupdf_raw:...` → extraction succeeded with basic quality, proceed to Step 2
- `WARN:...` → a tier failed, check if fallback succeeded
- `ASK_USER:...` → relay the message to the user and wait for their response
  - If user says "install" → run `pip install pymupdf4llm` and retry
  - If user says "continue" → proceed with whatever succeeded
  - If user provides a Markdown path → use that as paper.md, proceed to Step 2
- `ERROR:...` → all extraction failed, tell user and abort

After successful extraction, verify `<paper_dir>/paper.md` exists and is non-empty.

Extract the abstract:

1. Read the first 100 lines of `<paper_dir>/paper.md`
2. Find the abstract section (look for headings like "Abstract", "摘要", or the first substantial paragraph after the title/author block)
3. Write the abstract text to `<paper_dir>/abstract.md`

---

### Step 2: Create Agent Team

```
TeamCreate(team_name="paper-reader", description="Multi-agent paper reading: <paper title inferred from first page>")
```

Create tasks to track progress:

```
TaskCreate("Phase 0: Reviewer creates template")
TaskCreate("Phase 1: Reader fills template")
TaskCreate("Phase 2: Questioner Q&A with Reader")
TaskCreate("Phase 3: Reviewer arbitration and final report")
```

---

### Step 3: Phase 0 — Reviewer Creates Template

Spawn the Reviewer agent:

```
Agent(
  team_name="paper-reader",
  name="reviewer",
  subagent_type="general-purpose",
  prompt="""You are the Reviewer agent in a paper reading team. Follow the instructions in $SKILL_DIR/agents/reviewer_agent.md.

PAPER DIRECTORY: <paper_dir>
SKILL DIRECTORY: $SKILL_DIR

Execute Phase 0 ONLY. Read the full paper, read the generic template at $SKILL_DIR/templates/generic_cs_template.md, extend it with domain-specific guiding questions, and write template_extended.md. Do NOT fill in any content — only questions and structural guidance.

⚠️ Respect your role boundaries (see reviewer_agent.md §⛔). You are the Reviewer — do NOT fill template content or produce Reader/Questioner reports.

When done, send a message to the orchestrator: 'Phase 0 complete: template_extended.md written.'"""
)
```

Wait for the Reviewer to complete. Verify `<paper_dir>/template_extended.md` exists.

**Agent latency fallback:** If the Reviewer agent produces no output within ~5 minutes:
1. Send a status check message: `"Have you started reading the paper? Please report your progress."`
2. Wait 2 more minutes.
3. If still no `template_extended.md`: the orchestrator reads the paper and creates the template directly. Mark the phase as completed with a note: the final report should include `[ORCHESTRATOR_FALLBACK: Phase 0 template created by orchestrator due to Reviewer agent timeout]`.

If the agent fails, retry once before using fallback. Mark the task completed:

```
TaskUpdate(taskId="<phase0>", status="completed")
```

---

### Step 4: Phase 1 — Reader Fills Template

Spawn the Reader agent:

```
Agent(
  team_name="paper-reader",
  name="reader",
  subagent_type="general-purpose",
  prompt="""You are the Reader agent in a paper reading team. Follow the instructions in $SKILL_DIR/agents/reader_agent.md.

PAPER DIRECTORY: <paper_dir>
SKILL DIRECTORY: $SKILL_DIR

Execute Phase 1 ONLY. Read the full paper at <paper_dir>/paper.md. Read the template at <paper_dir>/template_extended.md. Fill every section with accurate, detailed content from the paper. Use exact numbers and direct quotes. Write reader_report.md.

⚠️ Respect your role boundaries (see reader_agent.md §⛔). You are the Reader — do NOT perform Reviewer or Questioner tasks.

When done, send a message to the orchestrator: 'Phase 1 complete: reader_report.md written.'"""
)
```

Wait for the Reader to complete. Verify `<paper_dir>/reader_report.md` exists.

**Agent latency fallback:** Same as Phase 0 — if Reader produces no output within ~5 minutes, send status check, wait 2 min, then orchestrator fills the template directly as fallback. Note as `[ORCHESTRATOR_FALLBACK: Phase 1 reader report created by orchestrator due to Reader agent timeout]`.

If the agent fails, retry once. Mark the task completed:

```
TaskUpdate(taskId="<phase1>", status="completed")
```

---

### Step 5: Phase 2 — Questioner Q&A with Reader

Spawn the Questioner agent:

```
Agent(
  team_name="paper-reader",
  name="questioner",
  subagent_type="general-purpose",
  prompt="""You are the Questioner agent in a paper reading team. Follow the instructions in $SKILL_DIR/agents/questioner_agent.md.

PAPER DIRECTORY: <paper_dir>
SKILL DIRECTORY: $SKILL_DIR

Execute Phase 2. Read the abstract at <paper_dir>/abstract.md. Read the Reader's report at <paper_dir>/reader_report.md. Read the reproducibility checklist at $SKILL_DIR/references/reproducibility_checklist.md.

Ask the Reader questions (via SendMessage, max 20) to fill any gaps needed to reproduce the paper. When done, produce your independent report at <paper_dir>/questioner_report.md following the same template structure.

⚠️ Respect your role boundaries (see questioner_agent.md §⛔). You are the Questioner — do NOT read the full paper, do NOT produce final_report.

When done, send a message to the orchestrator: 'Phase 2 complete: questioner_report.md written.'"""
)
```

**The Questioner and Reader will communicate peer-to-peer via SendMessage.** The Questioner sends questions to "reader", and the Reader responds to "questioner". This is automatic — you do not need to relay messages.

Wait for the Questioner to complete. Monitor by checking for `<paper_dir>/questioner_report.md`. The Questioner will self-determine when to stop (max 20 questions).

If the Questioner does not complete within a reasonable time (e.g., appears stuck), send a message asking for a status update.

Verify `<paper_dir>/questioner_report.md` exists. Mark the task completed:

```
TaskUpdate(taskId="<phase2>", status="completed")
```

---

### Step 6: Phase 3 — Reviewer Arbitration

Send the Reviewer agent Phase 3 instructions:

```
SendMessage(
  to="reviewer",
  summary="Phase 3 arbitration instructions",
  message="""Execute Phase 3 of reviewer_agent.md.

PAPER DIRECTORY: <paper_dir>

Read reader_report.md and questioner_report.md. Compare them section by section. For every inconsistency, consult paper.md for ground truth. If inconsistencies remain and the round limit (3) has not been reached, send directives to both the Reader and Questioner about what needs clarification. When consistent or round limit reached, produce final_report.md.

When done, send a message to the orchestrator: 'Phase 3 complete: final_report.md and summary_report.md written.'"""
)
```

Wait for the Reviewer to complete. If the Reviewer sends directives to the Reader/Questioner (triggering another Q&A sub-round), wait for them to update their reports, then the Reviewer will re-compare (up to 3 rounds total).

Verify `<paper_dir>/final_report.md` and `<paper_dir>/summary_report.md` exist. Mark the task completed:

```
TaskUpdate(taskId="<phase3>", status="completed")
```

---

### Step 7: Deliver Final Report

1. Read `<paper_dir>/final_report.md` and `<paper_dir>/summary_report.md` briefly to verify they are complete and well-formed.
2. Check for `[UNRESOLVED]` markers. If present, note them.
3. Deliver the paths and a brief summary to the user:

```
Paper reading complete.

Full report: <paper_dir>/final_report.md
Summary:      <paper_dir>/summary_report.md

Summary:
- Title: {title}
- Reproducibility: {score}
- Q&A exchanges: {count}
- Unresolved items: {count or "None"}
```

---

### Step 8: Cleanup

Send shutdown requests to all agents:

```
SendMessage(to="reviewer", message={"type": "shutdown_request", "reason": "Paper reading complete"})
SendMessage(to="reader", message={"type": "shutdown_request", "reason": "Paper reading complete"})
SendMessage(to="questioner", message={"type": "shutdown_request", "reason": "Paper reading complete"})
```

The task list serves as an audit trail — do not delete it.

## Error Handling

| Scenario | Action |
|----------|--------|
| Extraction script not found | Verify `$SKILL_DIR/scripts/extract_paper.py` exists. If not, the skill installation may be incomplete. |
| Extraction all methods fail | Ask user to provide a Markdown or text version of the paper. |
| paper.md is empty after extraction | The PDF may be image-only or corrupted. Ask user for a text version. |
| Agent spawn fails | Retry once with the same prompt. If it fails again, skip that phase and mark the corresponding report section as `[AGENT_FAILED]`. |
| Agent appears stuck (no output for extended time) | Send a message asking for status. If no response, retry once. |
| Questioner exceeds 20 questions | The Questioner agent self-limits to 20. If it appears to exceed this, send a reminder. |
| Reviewer exceeds 3 arbitration rounds | The Reviewer self-limits to 3 rounds. Force final report if beyond. |
| Phase file missing after agent claims completion | Ask the agent to re-write the file. If persists, mark as `[AGENT_FAILED]`. |
| Agent Team latency: Phase 0/1 agent produces no output within ~5 min | Send status check message. Wait 2 more minutes. If still no output, orchestrator executes the phase directly (manual fallback). Note in final report as `[ORCHESTRATOR_FALLBACK]`. |
| Agent Team latency: Phase 2 agents (Questioner/Reader) produce no Q&A within ~15 min | Send status check to both. If no response, ask user: "Agents appear unresponsive. Continue with manual Q&A or abort?" |
| System memory low during execution | Agents may fail to start or hang. Symptom: agents spawned but idle with no output. Recommendation: ensure ≥8 GB free RAM before running. |

## Notes

- The `$SKILL_DIR` environment variable is set by the Claude Code skill runner and points to the skill's root directory.
- All agent prompt files are at `$SKILL_DIR/agents/`. Substituting `<paper_dir>` with the actual path is critical — agents do not have access to the orchestrator's variables.
- The peer-to-peer Q&A in Phase 2 is the core value of this skill. Do not try to mediate — let the Questioner and Reader interact directly.
- If working with a paper that has already been read before (existing reports exist), ask the user if they want to overwrite or skip.

### ⚠️ Agent Team Latency

Agent Team members (Reviewer, Reader, Questioner) may experience **significant startup delay** (minutes) before they begin executing their prompts. This has been observed in practice and may be caused by:

1. **System resource constraints** — low available memory or high CPU load can slow agent initialization. Ensure sufficient free memory (≥8 GB recommended) before running this skill.
2. **Agent scheduling** — the Agent Team runtime schedules teammate agents with a built-in cooldown between turns. Expect 2-5 minutes before the first agent message is sent.
3. **Peer-to-peer message delivery** — messages between agents (SendMessage) are delivered asynchronously and may queue behind other pending messages.

**Mitigation strategies built into the orchestrator:**

- After spawning each agent, the orchestrator waits and polls for the expected output file rather than relying solely on agent messages.
- If an agent does not produce output within a reasonable window (~5 minutes for Phase 0/1, ~15 minutes for Phase 2 Q&A), the orchestrator sends a status check message.
- If Phase 0 or Phase 1 agents fail to produce output after a status check + 2-minute wait, the orchestrator falls back to executing the phase directly (manual mode) to keep the pipeline moving. The fallback is noted in the final report as `[ORCHESTRATOR_FALLBACK: Phase N executed by orchestrator due to agent timeout]`.
- Phase 2 (Q&A) has no orchestrator fallback — if the Questioner and Reader fail to interact, the orchestrator should ask the user whether to proceed with manual Q&A or abort.
