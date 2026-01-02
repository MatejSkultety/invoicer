# ADR-0001: SQLite schema initialization during startup (MVP)

## Status
Accepted

## Context
We need SQLite persistence for the MVP without adding migration tooling yet. The repo currently has no ORM or migration framework.

## Decision
For the MVP, each module initializes its own SQLite tables and indexes during app startup using `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS` statements.

## Consequences
- Fast bootstrap with minimal dependencies.
- Schema changes will require manual updates until migration tooling is introduced.
- Future work should introduce migrations before production use.
