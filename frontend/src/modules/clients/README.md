# Clients module (frontend)

Route: `/clients`

UI behavior:
- Lists clients with name, primary contact (with emoji), single-line notes preview (ellipsis), and a star badge for favourites.
- Client cards are derived on list refresh to avoid recomputing preview/contact strings on unrelated updates.
- Create client modal with validation feedback for required fields and favourite toggle.
- Notes textarea is fixed-size to keep the modal layout stable.
- Edit action reuses the modal with prefilled data.
- Archive action soft-deletes the client via the API.
- Success toasts on create/update/archive.
- Inline error message on API failures.
- Designed to remain usable on mobile browsers (stacked layout, touch-friendly controls).

Form fields:
- Required: name, address, city, country, main contact method, main contact.
- Optional: additional contact, IČO, DIČ, notes.

I18n:
- Module strings live in `frontend/src/modules/clients/i18n/en.js`.

Toast behavior:
- Uses shared toast store and host in `frontend/src/shared/`.

Manual verify:
1) Run the stack with `docker compose up --build`.
2) Navigate to `http://localhost:5173/clients`.
3) Create a client and verify it appears in the list.
4) Edit the client and confirm changes render.
5) Archive the client and confirm it disappears.

Testing:
- `npm run test` (Vitest + Vue Test Utils)
