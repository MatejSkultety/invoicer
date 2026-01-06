# Catalog items module (backend)

Base path: `/api/catalog-items`

## Endpoints
- `GET /api/catalog-items` list non-deleted catalog items
- `POST /api/catalog-items` create catalog item (201)
- `GET /api/catalog-items/{id}` fetch catalog item (404 if missing or deleted)
- `PUT /api/catalog-items/{id}` update catalog item (all fields required)
- `DELETE /api/catalog-items/{id}` soft delete catalog item (204)

## Data model
Fields:
- `id` uuid (text)
- `name` text (required, max 256)
- `description` text (required)
- `unit` text (required)
- `unit_price` integer (required, minor currency units)
- `tax_rate` integer (optional)
- `created_at` text
- `updated_at` text
- `deleted_at` text (nullable, soft delete)

Internal only:
- `created_by` text (auto-assigned; not exposed in API responses; currently defaults to `dev`)

## Manual verify
1) Run `docker compose up --build`.
2) `curl -X POST http://localhost:8000/api/catalog-items -H 'Content-Type: application/json' \
  -d '{"name":"Design work","description":"Product design services","unit":"hour","unit_price":15000,"tax_rate":21}'`
3) `curl http://localhost:8000/api/catalog-items`
4) `curl -X PUT http://localhost:8000/api/catalog-items/{id} -H 'Content-Type: application/json' \
  -d '{"name":"Design work updated","description":"Senior design services","unit":"hour","unit_price":20000,"tax_rate":null}'`
5) `curl -X DELETE http://localhost:8000/api/catalog-items/{id}`

Testing:
- `pytest`
