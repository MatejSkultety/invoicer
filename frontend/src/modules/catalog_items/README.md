# Catalog items module (frontend)

Route: `/catalog`

UI behavior:
- Lists catalog items with name and formatted price per unit, plus a one-line description preview.
- Create/edit modal with required fields and optional tax rate.
- Price input accepts decimals and converts to integer minor units on submit.
- Edit action reuses the modal with prefilled data.
- Archive action soft-deletes the item via the API.
- Success toasts on create/update/archive.
- Inline error message on API failures.
- Designed to remain usable on mobile browsers (stacked layout, touch-friendly controls).

Form fields:
- Required: name, description, unit, unit price.
- Optional: tax rate.
- Max lengths: name 256, description 1024, unit 64.

I18n:
- Module strings live in `frontend/src/modules/catalog_items/i18n/en.js`.

Toast behavior:
- Uses shared toast store and host in `frontend/src/shared/`.

Manual verify:
1) Run the stack with `docker compose up --build`.
2) Navigate to `http://localhost:5173/catalog`.
3) Create an item and verify it appears in the list.
4) Edit the item and confirm changes render.
5) Archive the item and confirm it disappears.

Testing:
- `npm run test` (Vitest + Vue Test Utils)
- Covered by `frontend/tests/catalog-items-page.test.js` and `frontend/tests/catalog-item-modal.test.js`.
