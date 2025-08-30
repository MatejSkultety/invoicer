# Branch Protection Setup

This repository uses branch protection to ensure proper code review processes.

## Setup Instructions

To enable branch protection for the `main` branch:

1. Go to **Settings** → **Branches** in your GitHub repository
2. Click **Add rule** 
3. Set **Branch name pattern** to `main`
4. Enable these settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals: 1**
   - ✅ **Require review from code owners**

This will ensure all changes to main require a pull request with approval from @MatejSkultety (as defined in CODEOWNERS).