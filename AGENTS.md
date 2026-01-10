# AGENTS.md — Repository instructions for coding agents (Codex/Copilot)

This file is the **single source of truth** for how AI coding agents should work in this repo.
Treat it like a “README for agents”: persistent context + non-negotiable rules + workflow.

> Important: When generating content intended to be committed, output **plain Markdown/code only**
> (no citations, no “source markers”, no hidden attribution tags).

---

## 0) Hard rules (non-negotiable)

### ASK FIRST — always
Before writing or changing code, you MUST:
1) Restate the goal (1–2 lines)
2) Ask clarifying questions (grouped; see Section 3)
3) Propose a small plan (2–6 bullets)
4) STOP and wait for answers

Only skip questions if:
- the user explicitly says: “Proceed with these assumptions: …”, OR
- the task is purely mechanical (formatting, rename, lint) with no product/architecture impact

### No secrets
- Never commit secrets (tokens, passwords, API keys).
- Do not paste secrets into code, docs, examples, or tests.

### Small, reviewable changes
- Keep PRs focused and minimal.
- Don’t mix refactors with features unless requested.

### Follow existing conventions
- If the repo already has tools/commands/style, follow them.
- If something is missing, propose a minimal improvement (prefer a separate PR).

---

## 1) Project reality (today)

- Localhost-first.
- No login/auth focus yet.
- MVP: **clients + invoices** (create, track, download).
- DB is **SQLite** now.
- Future direction: should be possible to evolve toward public usage later (e.g., multi-tenant),
  but do not overbuild early.

---

## 2) Repo structure (initial)

This is a monorepo with separate backend and frontend services.

- Backend: `backend/`
  - App code: `backend/app/`
  - Domain modules: `backend/app/modules/<module>/`
  - Tests: `backend/tests/`
- Frontend: `frontend/`
  - Source: `frontend/src/`
  - Domain modules: `frontend/src/modules/<module>/`
  - Shared utilities: `frontend/src/shared/`
  - Tests: `frontend/tests/`
- Architecture decisions: `docs/adr/`

Module names should mirror by **domain concept** only (e.g., `clients`, `invoices`).
Frontend and backend must NOT share code; they couple only via the API contract.

Do not introduce a new directory layout without discussing it first.

---

## 3) ASK-FIRST protocol (how to start every feature)

### 3.1 Required opening format (every time)
1) **Goal** (1–2 lines)
2) **Questions** (grouped; concise)
3) **Plan** (2–6 bullets)
4) **Wait** (do not implement yet)

### 3.2 Question checklist (use categories; ask what’s relevant)
**Goal & acceptance**
- What should be demonstrably working when this is “done”?
- Any UX constraints (flow, screens, “must look like X”)?

**Scope**
- Which side(s): backend, frontend, or both?
- What is explicitly out of scope for this branch?

**API / UI contract**
- Backend: endpoints, payloads, status codes, error format?
- Frontend: route/page, UI states, loading/error handling?
- Any backwards-compat expectations?

**Data & state**
- Which entities/fields are needed now vs later?
- Any uniqueness rules?
- Any state transitions/lifecycle rules?

**Edge cases**
- What happens on invalid input / missing data?
- Duplicate prevention? Concurrency concerns?

**Security & privacy**
- Any sensitive fields involved?
- Anything that must not be logged or returned by default?

**Ops / local dev**
- Any docker-compose changes needed?
- Any env vars to add? Default values?

**Testing**
- What’s the happy-path test?
- What’s the minimal negative/validation test?

**Docs**
- Which docs must be updated (module README, ADR, root README)?

### 3.3 If the user says “not sure”
- Offer 2–3 options with tradeoffs.
- Recommend a temporary default.
- Ask permission to proceed with that default.
- Document the choice as “tentative” in module docs (and ADR if significant).

---

## 4) Branch + thread workflow (mandatory)

For each feature:
1) Create branch: `feat/<module>-<short-desc>`
2) Use a fresh AI thread for that feature
3) Follow ASK-FIRST protocol
4) Implement code + tests + docs updates
5) Merge via PR

PR description must include:
- summary of behavior
- how to run/verify
- docs updated

---

## 5) Architecture rules (modular monolith + module boundaries)

Backend is a modular monolith:
- Each module owns its API routes, schemas, business logic, and persistence.
- Modules must not import other modules’ internal implementation details.
- Cross-module interaction happens through **public service interfaces**.

Frontend is modular by domain:
- Keep domain UI and API calls in `frontend/src/modules/<module>/`.
- Keep shared API client/utils/UI in `frontend/src/shared/`.
- Frontend should not embed backend business rules (backend is source of truth).
- Frontend features must be responsive for mobile browsers by default.
- User-facing strings should live in module i18n files and be accessed via the shared i18n helper.

Database:
- SQLite now; keep DB configuration externalized (env-driven).
- Avoid DB-specific assumptions in application logic.
- Store monetary values as integer cents (no floats) unless explicitly agreed otherwise.

---

## 6) Documentation rules (context preservation)

Every feature must update docs so future threads inherit context.

Preferred hierarchy:
1) Update/add a **module README** close to the code:
   - `backend/app/modules/<module>/README.md`
   - `frontend/src/modules/<module>/README.md`
2) If you made a significant or hard-to-reverse decision, write an **ADR** in `docs/adr/`.
3) Update root `README.md` only for big-picture “how to run” and project overview.

---

## 7) Testing expectations

Each feature should add at least:
- one happy-path test
- one negative/validation test

Keep tests fast and deterministic.
Avoid network calls unless explicitly requested.

---

## 8) Commands (discover, then standardize)

If the repo already defines commands (Makefile, scripts, task runner), use them.
If not, ask the user what style they prefer and propose minimal conventions.

Typical targets to document (once available):
- run backend
- run frontend
- run tests (backend + frontend)
- lint/format (backend + frontend)

---

## 9) End-of-response checklist (required)

After implementing a feature, end your response with:
- How to run/verify (commands)
- Tests added + how to run them
- Files changed
- Docs updated
- Follow-ups / TODOs (if any)

---

## 10) Optional: scoped agent instructions (future)

If you later add instructions inside subdirectories, keep them consistent and minimal.
Prefer pointing back to this root AGENTS.md to avoid conflicting guidance.
