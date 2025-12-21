# ADRs (Architecture Decision Records)

An Architecture Decision Record (ADR) captures a single architecturally significant decision,
including its context and consequences.

## When to write an ADR
Write an ADR when you are making a decision that:
- is hard to reverse (or expensive to change later), or
- affects multiple modules, or
- changes how the project will be developed/deployed long-term.

Examples:
- auth approach
- database migration strategy (SQLite → Postgres)
- API versioning strategy
- background jobs approach
- communications provider strategy

## Rules
- ADRs live in this folder: `docs/adr/`
- ADRs are never deleted; if a decision changes, create a new ADR and mark the old one as superseded.

## Naming convention
Use a sequential number + short kebab-case title:

`0001-short-title.md`
`0002-another-decision.md`

## Status values
Use one of:
- Proposed
- Accepted
- Rejected
- Deprecated
- Superseded by ADR-XXXX

## Template (copy/paste)

# ADR-0001: <Decision title>

## Status
Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-XXXX

## Context
What problem are we solving? What constraints matter? What forces/tradeoffs exist?

## Decision
What are we doing?

## Consequences
What becomes easier/harder? What do we need to follow up on?

## Alternatives considered (optional)
List 1–3 realistic alternatives and why they were not chosen.

## References (optional)
Links to issues, PRs, docs.
