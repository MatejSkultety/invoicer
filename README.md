# Invoicer

A modular, security-minded invoice management web app.

**Planned stack**
- Backend: FastAPI (Python)
- Frontend: Vue (likely Vue 3)
- Local orchestration: Docker Compose
- Database (now): SQLite
- Database (later): Postgres (goal: straightforward migration via configuration + migrations)

This repo is developed iteratively with AI (Codex/Copilot):
- one feature per branch
- one fresh AI thread per feature
- every feature updates docs so future AI threads inherit context automatically

## MVP scope (Phase 1)
- Client list (CRUD)
- Invoices:
  - create
  - track status
  - download as PDF
- Runs on localhost (no login/auth focus yet)

Non-goals for now:
- Multi-user roles/permissions
- Final choices for communications providers (email/Discord/WhatsApp). We’ll design seams first.

---

## Repository layout (initial)
This is a monorepo with two containers/services (backend + frontend). Module naming mirrors by *domain name* only.

```text
.
├─ README.md
├─ AGENTS.md
├─ docker-compose.yml
├─ docs/
│  └─ adr/
│     ├─ README.md
│     └─ 0001-example.md (optional)
├─ backend/
│  ├─ Dockerfile
│  ├─ pyproject.toml
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  └─ modules/
│  │     ├─ clients/
│  │     └─ invoices/
│  └─ tests/
└─ frontend/
   ├─ Dockerfile
   ├─ package.json
   └─ src/
      ├─ shared/
      └─ modules/
         ├─ clients/
         └─ invoices/

## Frontend responsiveness
All frontend features should be built to work well on mobile browsers (sensible defaults for small screens).
