# Users module (frontend)

Entry point: topbar preferences menu (⚙️) opens the profile modal.

Setup route: `/setup`

## Behavior
- Loads the current user profile from `GET /api/users/me` when the modal opens.
- Saves updates via `PUT /api/users/me` and shows a toast on success.
- When no profile is present, the app routes to `/setup` and blocks the rest of the UI.

## Fields
All required:
- `name`
- `address`
- `city`
- `country`
- `trade_licensing_office`
- `ico`
- `dic`
- `email`
- `phone`
- `bank`
- `iban`
- `swift`

Notes:
- The UI expects all fields to be filled before saving.
- `GET /api/users/me` can return partial data from older records.

## Files
- UI: `frontend/src/modules/users/UsersMenu.vue`, `frontend/src/modules/users/UserProfileModal.vue`, `frontend/src/modules/users/SetupProfilePage.vue`
- API: `frontend/src/modules/users/api.js`
- Profile helpers: `frontend/src/modules/users/profile.js`
- Strings: `frontend/src/modules/users/i18n/en.js`

## Manual verify
1) Run backend and frontend.
2) If no profile exists, the app shows `/setup`.
3) Fill all fields and click Save.
4) Confirm you land on the home page and can access clients/catalog.

Testing:
- `npm run test`
