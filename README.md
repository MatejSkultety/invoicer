# Invoicer

A modular, security-minded invoice management web app.

- Backend: FastAPI (planned)
- Frontend: Vue (planned)
- Local orchestration: docker-compose (planned)
- Database (now): SQLite
- Database (later): Postgres (goal: straightforward migration via configuration + migrations)

This repo is developed iteratively with AI (Codex/Copilot):
- one feature per branch
- one fresh AI thread per feature
- each feature updates docs so future threads inherit context automatically

## MVP scope (Phase 1)
- Client list (CRUD)
- Invoices:
  - create
  - track status
  - **download as PDF**
- Runs on localhost (no login focus yet)

Non-goals for now:
- Multi-user roles/permissions
- Final choices for communications providers (email/Discord/WhatsApp). We’ll design seams first.

## Architecture idea (high-level)
We build a **modular monolith** first:
- one backend deployable
- strict internal boundaries between modules
- scalable structure that can later evolve (including multi-tenant support)

We avoid committing to a fixed folder structure early. Instead, we enforce *boundary rules*:
- modules have their own API + schemas + business logic + persistence access
- modules don’t reach into each other’s internals directly
- cross-module interaction happens through public service interfaces

## Database: SQLite now, Postgres later
SQLite is used for early development. The codebase should avoid SQLite-only assumptions and keep DB configuration externalized, so switching to Postgres later is mostly:
- config change
- migrations
- small compatibility fixes (if any)

## AI-assisted workflow
The “default instructions” for Codex/Copilot live in **AGENTS.md** (source of truth)

### Branching
For each feature:
1. Create a branch: `feature/<module>-<short-desc>`
2. Start a new Codex/Copilot thread for that branch
3. Discuss → implement → merge via PR

### Documentation evolves with the code
Every feature must update docs so future AI threads have context:
- lightweight module docs (behavior, API, flows)
- ADRs for significant decisions

Architecture Decision Records (ADRs) are a common lightweight pattern to record decisions and rationale
## License
GNU license (see `LICENSE`)
