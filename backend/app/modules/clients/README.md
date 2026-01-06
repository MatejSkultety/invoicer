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
- `city` text (required)
- `country` text (required)
- `main_contact_method` text (required, enum: email/whatsapp/discord)
- `main_contact` text (required)
- `additional_contact` text (optional)
- `ico` text (optional)
- `dic` text (optional)
- `notes` text (optional)
- `favourite` boolean (required, defaults false)
- `created_at` text
- `updated_at` text
- `deleted_at` text (nullable, soft delete)

Internal only:
- `created_by` text (auto-assigned; not exposed in API responses; currently defaults to `dev`)

## Manual verify
1) Run `docker compose up --build`.
2) `curl -X POST http://localhost:8000/api/clients -H 'Content-Type: application/json' \
  -d '{"name":"Acme","address":"123 Main","city":"Prague","country":"Czechia","main_contact_method":"email","main_contact":"hello@acme.test","notes":"Priority","favourite":false}'`
3) `curl http://localhost:8000/api/clients`
4) `curl -X PUT http://localhost:8000/api/clients/1 -H 'Content-Type: application/json' \
  -d '{"name":"Acme Co","address":"123 Main","city":"Brno","country":"Czechia","main_contact_method":"whatsapp","main_contact":"+420123456789","notes":null,"favourite":true}'`
5) `curl -X DELETE http://localhost:8000/api/clients/1`

Testing:
- `pytest`
