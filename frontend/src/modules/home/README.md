# Home module (frontend)

Route: `/`

## Behavior
- Placeholder home dashboard shown after a company profile is completed.
- Gated behind the profile setup flow.

## Files
- UI: `frontend/src/modules/home/HomePage.vue`
- Strings: `frontend/src/modules/home/i18n/en.js`

## Manual verify
1) Complete the company profile setup.
2) Navigate to `http://localhost:5173/`.

Testing:
- `npm run test`
