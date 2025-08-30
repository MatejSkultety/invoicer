#!/usr/bin/env python3
"""
Branch Protection Setup Script

This script configures branch protection rules for the repository using the GitHub API.
Requires a GitHub token with appropriate permissions.

Usage:
    python setup_branch_protection.py

Environment Variables:
    GITHUB_TOKEN: GitHub personal access token with repo permissions
    GITHUB_REPO: Repository in format "owner/repo" (optional, will detect from git)
"""

import json
import os
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_github_token():
    """Get GitHub token from environment."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub personal access token:")
        print("export GITHUB_TOKEN=your_token_here")
        sys.exit(1)
    return token


def get_repository():
    """Get repository name from environment or git remote."""
    repo = os.getenv("GITHUB_REPO")
    if repo:
        return repo

    try:
        # Try to get from git remote
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        remote_url = result.stdout.strip()

        # Parse GitHub URL
        if "github.com" in remote_url:
            if remote_url.startswith("https://github.com/"):
                repo_path = remote_url.replace("https://github.com/", "").replace(
                    ".git", ""
                )
            elif remote_url.startswith("git@github.com:"):
                repo_path = remote_url.replace("git@github.com:", "").replace(
                    ".git", ""
                )
            else:
                raise ValueError("Unrecognized GitHub URL format")
            return repo_path
        else:
            raise ValueError("Not a GitHub repository")
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error detecting repository: {e}")
        print("Please set GITHUB_REPO environment variable (format: owner/repo)")
        sys.exit(1)


def make_github_request(url, token, method="GET", data=None):
    """Make a GitHub API request."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    if data:
        data = json.dumps(data).encode("utf-8")

    request = Request(url, data=data, headers=headers)
    request.get_method = lambda: method

    try:
        with urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}")
        raise
    except URLError as e:
        print(f"URL Error: {e}")
        raise


def setup_branch_protection(token, repo, branch="main"):
    """Set up branch protection rules."""
    url = f"https://api.github.com/repos/{repo}/branches/{branch}/protection"

    protection_config = {
        "required_status_checks": {"strict": True, "contexts": ["lint-and-test"]},
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "require_last_push_approval": False,
        },
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }

    print(f"Setting up branch protection for {repo}:{branch}")
    print("Configuration:")
    print(json.dumps(protection_config, indent=2))

    try:
        result = make_github_request(url, token, method="PUT", data=protection_config)
        print("✅ Branch protection configured successfully!")
        return result
    except HTTPError as e:
        if e.code == 404:
            print(f"❌ Repository {repo} or branch {branch} not found")
            print("Please check the repository name and ensure the branch exists")
        elif e.code == 403:
            print("❌ Insufficient permissions to configure branch protection")
            print(
                "Please ensure your token has 'repo' permissions and you have admin access"
            )
        else:
            print(f"❌ Failed to configure branch protection: HTTP {e.code}")
        raise


def verify_protection(token, repo, branch="main"):
    """Verify that branch protection is configured."""
    url = f"https://api.github.com/repos/{repo}/branches/{branch}/protection"

    try:
        protection = make_github_request(url, token)
        print("\n📋 Current branch protection settings:")

        # Check required status checks
        if protection.get("required_status_checks"):
            print("✅ Required status checks: enabled")
            contexts = protection["required_status_checks"].get("contexts", [])
            print(f"   Contexts: {', '.join(contexts) if contexts else 'none'}")
            strict = protection["required_status_checks"].get("strict", False)
            print(f"   Strict (up-to-date): {'enabled' if strict else 'disabled'}")
        else:
            print("❌ Required status checks: disabled")

        # Check PR reviews
        if protection.get("required_pull_request_reviews"):
            reviews = protection["required_pull_request_reviews"]
            count = reviews.get("required_approving_review_count", 0)
            print(f"✅ Required PR reviews: {count} approval(s)")
            dismiss = reviews.get("dismiss_stale_reviews", False)
            print(f"   Dismiss stale reviews: {'enabled' if dismiss else 'disabled'}")
        else:
            print("❌ Required PR reviews: disabled")

        # Check admin enforcement
        enforce_admins = protection.get("enforce_admins", {}).get("enabled", False)
        print(
            f"{'✅' if enforce_admins else '❌'} Enforce for administrators: {'enabled' if enforce_admins else 'disabled'}"
        )

        return True
    except HTTPError as e:
        if e.code == 404:
            print(f"❌ No branch protection configured for {branch}")
            return False
        else:
            raise


def main():
    """Main function."""
    print("🔒 GitHub Branch Protection Setup")
    print("=" * 40)

    # Get configuration
    token = get_github_token()
    repo = get_repository()

    print(f"Repository: {repo}")
    print(f"Branch: main")

    # Check current protection status
    print("\n🔍 Checking current protection status...")
    try:
        has_protection = verify_protection(token, repo)

        if has_protection:
            response = input("\nBranch protection already exists. Update it? (y/N): ")
            if response.lower() != "y":
                print("Aborted.")
                return

        # Set up protection
        print("\n⚙️  Configuring branch protection...")
        setup_branch_protection(token, repo)

        # Verify setup
        print("\n🔍 Verifying configuration...")
        verify_protection(token, repo)

        print("\n🎉 Branch protection setup completed!")
        print("\nNext steps:")
        print("1. Test by trying to push directly to main (should be blocked)")
        print("2. Create a feature branch and pull request")
        print("3. Verify that approval is required before merging")

    except (HTTPError, URLError) as e:
        print(f"\n❌ Failed to configure branch protection: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
