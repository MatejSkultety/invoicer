# AGENTS.md — Instructions for coding agents (Codex/Copilot)

AGENTS.md is the persistent “README for agents”: a predictable place to store project context and rules so new AI threads don’t start from zero. :contentReference[oaicite:3]{index=3}

Use this file as the single source of truth for how to work in this repository.

---

## 1) Project reality (today)
- Localhost-first. Do not optimize for production deployment yet unless asked.
- No login/auth focus yet.
- MVP: clients + invoices (create + track + download).
- DB is SQLite right now.
- Future direction: ability to evolve toward “public” usage later (multi-tenant readiness), but we will not overbuild early.

---

## 2) How we work (mandatory workflow)
For each feature:
1. Work in a dedicated branch: `feature/<module>-<short-desc>`
2. Use a new AI thread per feature.
3. First respond with **questions** (see “ASK-FIRST protocol”).
4. Only after questions are answered, implement:
   - code changes
   - tests
   - docs updates (so future threads keep context)
5. End with:
   - how to run tests (or what you attempted)
   - list of files changed

Keep PRs small and reviewable.

---

## 3) ASK-FIRST protocol (non-negotiable)
Agents MUST ask clarifying questions before writing code.

The only exceptions:
- The user explicitly says “proceed with assumptions” (and lists them), OR
- The task is purely mechanical (formatting, renaming files, fixing lint) and has no product/architecture impact.

### 3.1 Required behavior
Before implementing, do the following in order:

A) **Restate the goal** in 1–2 lines (what will be delivered).
B) **Ask clarifying questions**, grouped by category below.
C) **Propose a small plan** with 2–6 bullets.
D) Wait for answers. Do not start coding yet.

### 3.2 Question checklist (use these categories every time)
Ask only what’s relevant, but always cover categories that apply.

**Product / UX**
- What is the desired user flow?
- What are the success criteria (what should I demo when done)?
- Any constraints (performance, offline use, “must look like X”)?

**API contract**
- New endpoints? payload shape? versioning?
- Expected error cases and error format?
- Backwards compatibility expectations?

**Data model**
- What entities/fields are needed now vs later?
- Any uniqueness rules, lifecycle/status rules?
- Any migration concerns (existing data)?

**Edge cases**
- What should happen when data is missing/invalid?
- Concurrency or duplicates?
- What should be allowed vs rejected?

**Security / privacy**
- Any sensitive fields involved?
- Logging rules (what must never be logged)?
- Any authorization boundaries even in localhost mode?

**Operational concerns**
- Should this run purely in-process or needs a background job?
- Any docker-compose implications?

**Testing**
- What should be unit-tested vs integration-tested?
- What is the minimum test coverage for this feature?

**Documentation**
- What new behavior must be documented?
- Is this a “decision” that needs an ADR?

### 3.3 If the user doesn’t know yet
If the user answers “not sure”:
- propose 2–3 options with tradeoffs
- recommend one *temporary default*
- document the decision as “tentative” in docs
- do NOT hardcode a permanent choice

---

## 4) Architecture rules (modular monolith, boundaries)
We build a modular monolith first, with strict module boundaries.

Boundary rules:
- Modules may not import other modules’ internal implementation details.
- Cross-module interaction happens through public service interfaces (or explicit shared abstractions).
- Shared infrastructure (config, logging, db session) must stay in a clearly identified “core” area, wherever it lives in the repo.

Do not impose a directory layout if one does not exist. Instead, maintain boundaries using:
- clear package/module naming
- explicit interfaces
- disciplined imports
- tests

---

## 5) Commands, testing, structure, style, git workflow, boundaries
Keep instructions here aligned with what exists in the repo. GitHub recommends these core areas for effective agents.md files. :contentReference[oaicite:4]{index=4}

### Commands
- If commands are documented in the repo, follow them.
- If not, discover how to run the project from existing files and propose improvements (don’t invent complicated tooling).

### Testing
- Always add at least:
  - one happy-path test
  - one negative/validation test
- Prefer fast, deterministic tests.
- If the repo lacks a test runner, propose a minimal setup (smallest useful change).

### Code style
- Follow existing conventions in the repo.
- If none exist, propose minimal lint/format tooling in a separate PR (don’t bundle it into unrelated features).

### Git workflow
- Keep commits scoped and readable.
- PR description must include:
  - summary
  - how to test
  - docs updated

### Boundaries
- Enforce module boundaries via imports + interfaces.
- If a feature cuts across modules, document the boundary and keep responsibilities clear.

---

## 6) Documentation rule (context preservation)
Every feature must update docs so future AI threads have context.

Preferred lightweight approach:
- Add/extend a module doc explaining behavior/API/flows.
- For significant decisions, write an ADR (context → decision → consequences is a common template). :contentReference[oaicite:5]{index=5}

---

## 7) Copilot/Codex instruction files
Some tools also read repository instruction files such as:
- `.github/copilot-instructions.md`
- other GitHub instruction file locations

If those exist, keep them minimal and point back to AGENTS.md to avoid conflicting rules. :contentReference[oaicite:6]{index=6}
