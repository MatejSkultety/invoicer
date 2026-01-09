# Users module (frontend)

Entry point: topbar preferences menu (⚙️) opens the profile modal.

## Behavior
- Loads the current user profile from `GET /api/users/me` when the modal opens.
- Saves updates via `PUT /api/users/me` and shows a toast on success.
- If the profile cannot be loaded, the form is disabled and an error banner is shown.

## Fields
Required:
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
- UI: `frontend/src/modules/users/UsersMenu.vue`, `frontend/src/modules/users/UserProfileModal.vue`
- API: `frontend/src/modules/users/api.js`
- Strings: `frontend/src/modules/users/i18n/en.js`

## Manual verify
1) Run backend and frontend.
2) Click the ⚙️ menu in the topbar and choose "Company profile".
3) Edit fields and click Save.

Testing:
- `npm run test`
