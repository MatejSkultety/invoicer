# invoicer

A Python invoicing application.

## Development

This repository uses branch protection rules to ensure code quality and proper review processes.

### Branch Protection

The `main` branch is protected with the following requirements:
- All changes must be made through pull requests
- Pull requests require at least 1 approval before merging
- Status checks must pass (linting, formatting, tests)
- Branches must be up to date before merging

See [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) for detailed setup instructions.

### Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all linting and tests pass locally
4. Submit a pull request
5. Request review and wait for approval
6. Merge after approval and passing status checks

### CI/CD

The repository includes automated workflows for:
- **Linting**: Code quality checks with flake8
- **Formatting**: Code formatting verification with black
- **Import sorting**: Import organization with isort
- **Testing**: Automated test execution (when tests are present)
- **Multi-version testing**: Python 3.9, 3.10, 3.11, and 3.12 support