# Branch Protection Setup

This repository requires branch protection rules to ensure code quality and proper review processes. Since branch protection rules must be configured through GitHub's repository settings or API, this document provides instructions for setting up the required protection.

## Required Branch Protection Settings

### 1. Protect Main Branch

To protect the `main` branch, configure the following settings in GitHub:

**Repository Settings → Branches → Add rule for `main`:**

#### Basic Protection
- ✅ **Restrict pushes that create files larger than 100MB**
- ✅ **Require a pull request before merging**
- ✅ **Require approvals: 1** (minimum required)
- ✅ **Dismiss stale PR approvals when new commits are pushed**
- ✅ **Require review from code owners** (if CODEOWNERS file exists)

#### Status Checks (if CI workflows are available)
- ✅ **Require status checks to pass before merging**
- ✅ **Require branches to be up to date before merging**
- Select required status checks:
  - `lint-and-test` (from CI workflow)

#### Additional Restrictions
- ✅ **Restrict pushes that create files larger than 100MB**
- ✅ **Do not allow bypassing the above settings**
- ✅ **Include administrators** (apply rules to repository administrators)

### 2. Manual Setup via GitHub Web Interface

1. Go to your repository on GitHub
2. Click **Settings** (requires admin access)
3. Click **Branches** in the left sidebar
4. Click **Add rule**
5. Set **Branch name pattern** to `main`
6. Configure the protection settings as listed above
7. Click **Create**

### 3. Automated Setup via GitHub CLI

If you have GitHub CLI installed and appropriate permissions:

```bash
# Install GitHub CLI if not already installed
# See: https://github.com/cli/cli#installation

# Set up branch protection rule
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["lint-and-test"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null
```

### 4. Automated Setup via GitHub API

See the included `setup_branch_protection.py` script for programmatic setup using the GitHub API.

## Status Checks

The repository includes a CI workflow (`.github/workflows/ci.yml`) that provides:

- **Python linting** with flake8
- **Code formatting** checks with black
- **Import sorting** checks with isort
- **Test execution** (when tests are present)
- **Multi-version Python support** (3.9, 3.10, 3.11, 3.12)

This workflow will run on all push and pull request events to the main branch and can be used as a required status check.

## CODEOWNERS (Optional)

To require specific reviewers for certain files or directories, create a `.github/CODEOWNERS` file:

```
# Global owners
* @MatejSkultety

# Specific paths (examples)
# *.py @MatejSkultety
# /docs/ @MatejSkultety
```

## Verification

After setting up branch protection:

1. Try to push directly to main (should be blocked)
2. Create a feature branch and PR
3. Verify that approval is required before merging
4. Verify that status checks must pass (if configured)

## Troubleshooting

- **Admin bypass**: Ensure "Include administrators" is enabled to prevent accidental bypassing
- **Status checks not appearing**: Ensure the CI workflow has run at least once to register the status check
- **Permission issues**: Repository admin access is required to configure branch protection