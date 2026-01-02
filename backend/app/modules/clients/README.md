# Clients module (backend)

Base path: `/api/clients`

## Endpoints
- `GET /api/clients` list non-deleted clients
- `POST /api/clients` create client (201)
- `GET /api/clients/{id}` fetch client (404 if missing or deleted)
- `PUT /api/clients/{id}` update client (all fields required)
- `DELETE /api/clients/{id}` soft delete client (204)

## Data model
Fields:
- `id` integer
- `name` text (required)
- `address` text (required)
- `email` text (required, unique among non-deleted)
- `notes` text (required)
- `created_at` text
- `updated_at` text
- `deleted_at` text (nullable, soft delete)

Uniqueness:
- Enforced with a partial unique index on `lower(email)` for rows with `deleted_at IS NULL`.
- Guarded in the service layer to return a 409 conflict.

## Manual verify
1) Run `docker compose up --build`.
2) `curl -X POST http://localhost:8000/api/clients -H 'Content-Type: application/json' \
  -d '{"name":"Acme","address":"123 Main","email":"hello@acme.test","notes":"Priority"}'`
3) `curl http://localhost:8000/api/clients`
4) `curl -X PUT http://localhost:8000/api/clients/1 -H 'Content-Type: application/json' \
  -d '{"name":"Acme Co","address":"123 Main","email":"hello@acme.test","notes":"Updated"}'`
5) `curl -X DELETE http://localhost:8000/api/clients/1`

Testing:
- `pytest`
