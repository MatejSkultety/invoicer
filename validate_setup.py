#!/usr/bin/env python3
"""
Validation script to check that all branch protection files are properly configured.
"""

import os
import sys

import yaml


def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (missing)")
        return False


def check_yaml_syntax(filepath, description):
    """Check if a YAML file has valid syntax."""
    try:
        with open(filepath, "r") as f:
            yaml.safe_load(f)
        print(f"✅ {description}: Valid YAML syntax")
        return True
    except yaml.YAMLError as e:
        print(f"❌ {description}: Invalid YAML syntax - {e}")
        return False
    except FileNotFoundError:
        print(f"❌ {description}: File not found")
        return False


def main():
    """Main validation function."""
    print("🔍 Branch Protection Setup Validation")
    print("=" * 40)

    all_good = True

    # Check essential files
    files_to_check = [
        (".github/workflows/ci.yml", "CI Workflow"),
        (
            ".github/workflows/branch-protection-check.yml",
            "Branch Protection Check Workflow",
        ),
        (".github/CODEOWNERS", "Code Owners File"),
        ("setup_branch_protection.py", "Branch Protection Setup Script"),
        ("BRANCH_PROTECTION.md", "Branch Protection Documentation"),
        ("README.md", "Updated README"),
    ]

    print("\n📁 File Existence Check:")
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False

    # Check YAML syntax
    print("\n📋 YAML Syntax Check:")
    yaml_files = [
        (".github/workflows/ci.yml", "CI Workflow YAML"),
        (
            ".github/workflows/branch-protection-check.yml",
            "Branch Protection Check YAML",
        ),
    ]

    for filepath, description in yaml_files:
        if not check_yaml_syntax(filepath, description):
            all_good = False

    # Check Python script syntax
    print("\n🐍 Python Script Check:")
    try:
        import py_compile

        py_compile.compile("setup_branch_protection.py", doraise=True)
        print("✅ Branch Protection Script: Valid Python syntax")
    except py_compile.PyCompileError as e:
        print(f"❌ Branch Protection Script: Invalid Python syntax - {e}")
        all_good = False

    # Summary
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All checks passed! Branch protection setup is ready.")
        print("\nNext steps:")
        print("1. Merge this PR to enable the CI workflows")
        print("2. Configure branch protection rules (see BRANCH_PROTECTION.md)")
        print("3. Test the protection by creating a feature branch and PR")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
