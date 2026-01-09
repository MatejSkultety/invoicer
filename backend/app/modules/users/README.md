# Users module (backend)

Base path: `/api/users`

## Endpoints
- `GET /api/users/me` fetch the local user profile (404 if missing)
- `PUT /api/users/me` upsert the local user profile

## Data model
Fields:
- `id` text (fixed to `local-user` for the single local user)
- `name` text (required, max 256)
- `address` text (required, max 256)
- `city` text (required, max 128)
- `country` text (required, max 128)
- `trade_licensing_office` text (required, max 256)
- `ico` text (required, max 32)
- `dic` text (required, max 32)
- `email` text (required, max 256)
- `phone` text (required, max 64)
- `bank` text (required, max 256)
- `iban` text (required, max 34)
- `swift` text (required, max 11)
- `created_at` text
- `updated_at` text

Notes:
- `PUT /api/users/me` requires all fields to be present and non-empty.
- `GET /api/users/me` returns any stored values, even if some fields are missing.

## Manual verify
1) Run `docker compose up --build`.
2) `curl -X PUT http://localhost:8000/api/users/me -H 'Content-Type: application/json' \
  -d '{"name":"Acme Co","address":"123 Main","city":"Prague","country":"Czechia","trade_licensing_office":"Prague 1","ico":"12345678","dic":"CZ12345678","email":"billing@acme.test","phone":"+420123456789","bank":"Example Bank","iban":"CZ6508000000192000145399","swift":"GIBACZPX"}'`
3) `curl http://localhost:8000/api/users/me`

Testing:
- `pytest`
