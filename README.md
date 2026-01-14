# GanttPRO API Test Suite

Complete automated test suite for GanttPRO API v1.0, built with Python and pytest.

## Features

- 137 comprehensive tests covering 11 API endpoints
- Organized by API module (Tasks, Comments, Attachments, Links, Timelogs, etc.)
- Multiple test types: positive, auth, validation, logic, defaults, boundaries
- HTML + Allure + JUnit XML reports
- GitHub Actions CI/CD with automated testing and reporting
- Centralized configuration and environment management
- Auto-generated test navigation index

## Quick Start

### Prerequisites
- Python 3.9+
- pip or conda

### Setup

1. Clone and enter directory:
   ```bash
   git clone https://github.com/Alexsander13/api-tests-ganttpro.git
   cd api-tests-ganttpro
   ```

2. Create Python environment:
   ```bash
   # Using venv (recommended)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Using conda
   conda create -n ganttpro-tests python=3.9
   conda activate ganttpro-tests
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your API_KEY and BASE_URL
   ```

5. Run tests:
   ```bash
   pytest
   ```

## Test Coverage

Current test suite: 137 tests covering 11/35 API endpoints (31.4% coverage)

| Module | Tests | Assertions | Status |
|--------|-------|-----------|--------|
| Tasks | 25 | 59 | ✅ |
| Comments | 15 | 35 | ✅ |
| Attachments | 12 | 28 | ✅ |
| Links | 14 | 32 | ✅ |
| Timelogs | 20 | 47 | ✅ |
| Other Endpoints | 51 | 46 | ✅ |
| TOTAL | 137 | 247 | ✅ |

## Running Tests

### All Tests
```bash
pytest
```

### Specific Module
```bash
pytest tests/endpoints/tasks/
```

### By Test Type (Tag)
```bash
pytest -m "positive"           # Only positive tests
pytest -m "auth"              # Only auth tests
pytest -m "POST"              # Only POST method tests
pytest -m "positive and POST"  # Positive POST tests
```

### Available Tags
- HTTP Methods: POST, GET, PUT, DELETE
- Test Types: positive, auth, validation, logic, defaults, boundaries

### With Detailed Output
```bash
pytest -v                      # Verbose output
pytest -s                      # Show print statements
pytest -vv                     # Extra verbose
```

### Generate Reports

HTML Report:
```bash
pytest --html=reports/report.html --self-contained-html
```

Allure Report (Recommended):
```bash
pytest --alluredir=./allure-results
python open_allure.py  # Opens in browser on http://localhost:8000
```

Coverage Report:
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Project Structure

```
api-tests-ganttpro/
├── .github/
│   ├── workflows/
│   │   ├── tests.yml              # GitHub Actions test workflow
│   │   └── publish-reports.yml    # Report publishing workflow
│   └── dependabot.yml             # Automated dependency updates
├── src/
│   ├── config.py                  # Environment configuration
│   ├── http_client.py             # HTTP client wrapper
│   ├── spec_loader.py             # API specification loader
│   ├── assertions.py              # Reusable assertion helpers
│   └── navigation/
│       ├── TEST_INDEX.md          # Auto-generated test index
│       └── generate_test_index.py
├── tests/
│   ├── conftest.py                # Shared pytest fixtures
│   ├── endpoints/                 # Endpoint tests (137 tests)
│   │   ├── tasks/                 # Task endpoint tests (25)
│   │   ├── comments/              # Comment endpoint tests (15)
│   │   ├── attachments/           # Attachment tests (12)
│   │   ├── links/                 # Link tests (14)
│   │   ├── timelogs/              # Timelog tests (20)
│   │   └── ...other endpoints/
│   ├── smoke/                     # Quick smoke tests
│   └── scenarios/                 # Integration scenarios
├── allure-results/                # Allure report data (auto-generated)
├── reports/                       # Test reports (auto-generated)
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── open_allure.py                 # HTTP server for Allure reports
├── api_spec.json                  # GanttPRO API specification
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore patterns
└── README.md                      # This file
```

## Environment Configuration

### Required Variables

Create .env file (copy from .env.example):

```env
BASE_URL=https://api.ganttpro.com/v1.0
API_KEY=your_ganttpro_api_key_here
```

### Optional Variables

Add these to enable additional tests (tests skip if missing):

```env
TASK_ID=123456789
PROJECT_ID=987654321
COMMENT_ID=111111111
TIMELOG_ID=222222222
LINK_ID=333333333
ATTACHMENT_ID=444444444
RESOURCE_ID=555555555
USER_ID=666666666
```

## GitHub Actions CI/CD

This project includes automated testing and reporting via GitHub Actions.

### Workflows

.github/workflows/tests.yml - Main Test Execution
- Triggers: Push to main/develop, Pull requests, Daily schedule (9:00 UTC)
- Runs: Tests on macOS-latest
- Artifacts: Allure results, JUnit XML, Coverage reports
- View: GitHub Actions tab → Tests workflow

.github/workflows/publish-reports.yml - Report Publishing
- Triggers: After tests.yml completes
- Publishes: Allure reports to GitHub Pages
- Setup: Enable GitHub Pages in repo settings (optional)

### Setting Up GitHub Secrets

For GitHub Actions to run tests, you must configure secrets:

1. Go to your repository Settings → Secrets and variables → Actions
2. Click New repository secret
3. Add the following secrets:

| Secret Name | Value | Required |
|-------------|-------|----------|
| API_KEY | Your GanttPRO API key | Yes |
| BASE_URL | API base URL | No (defaults to https://api.ganttpro.com/v1.0) |

### Optional: GitHub Pages Setup

To publish Allure reports to GitHub Pages:

1. Go to repository Settings → Pages
2. Under Build and deployment:
   - Source: Select Deploy from a branch
   - Branch: Select gh-pages
   - Folder: Select /root
3. Save settings
4. After workflow runs, reports available at: https://Alexsander13.github.io/api-tests-ganttpro/

## Test Reports

### Allure Report (Recommended)

```bash
# Run tests and generate Allure results
pytest --alluredir=./allure-results

# Open in browser
python open_allure.py
```

Browser opens to http://localhost:8000 with interactive report.

### HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
open reports/report.html
```

### Coverage Report

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### JUnit XML

```bash
pytest --junit-xml=reports/junit.xml
```

## Troubleshooting

### Tests Fail with "401 Unauthorized"
- Verify API_KEY in .env is correct
- Check API key has not expired
- Confirm BASE_URL is correct for your GanttPRO instance

### Tests Skip During Execution
- Tests skip if optional environment variables are missing
- Add required IDs to .env file to enable full test coverage
- Run pytest -v to see which tests are skipped and why

### Allure Report Will Not Load
- Ensure HTTP server is running: python open_allure.py
- Check port 8000 is free: lsof -i :8000
- If opening via file protocol, use HTTP server instead

### Tests Timeout
- Increase timeout in pytest.ini
- Check network connectivity to API
- Verify API is not rate limiting
- Check endpoint availability

### Module Not Found
- Ensure Python environment is activated
- Reinstall dependencies: pip install -r requirements.txt
- Check Python version: python --version (must be 3.9+)

## Development

### Adding New Tests

1. Create test file in appropriate endpoint directory:
   ```bash
   tests/endpoints/module_name/test_feature.py
   ```
2. Use template from existing tests in same directory
3. Add Allure decorators:
   ```python
   import pytest
   import allure

   @allure.feature('Module Name')
   @allure.story('Feature Description')
   @pytest.mark.positive
   @pytest.mark.POST
   def test_create_success():
       """Test creating resource successfully"""
       # test code
   ```
4. Run your new test:
   ```bash
   pytest tests/endpoints/module_name/test_feature.py -v
   ```
5. Commit and push:
   ```bash
   git add tests/endpoints/module_name/test_feature.py
   git commit -m "feat: add new endpoint tests for module"
   git push origin feature/add-tests
   ```

### Test Naming Convention
- Format: test_{method}_{operation}_{result}
- Examples: test_create_success, test_update_forbidden, test_list_invalid_params, test_delete_not_found

### Code Style
- Follow PEP 8
- Use type hints for function parameters
- Add docstrings to complex functions
- Use descriptive variable names
- Keep tests focused and independent

### Running Tests Before Commit
```bash
pytest
pytest --cov=src
pytest tests/endpoints/tasks/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/add-new-tests
   ```
3. Make changes and add tests
4. Run tests to verify:
   ```bash
   pytest
   ```
5. Commit with meaningful message:
   ```bash
   git commit -m "feat: add new endpoint tests for feature"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/add-new-tests
   ```
7. Create Pull Request with test results

## Pushing to GitHub

### First Time Setup
```bash
git init
git add .
git commit -m "Initial commit: Add GanttPRO API test suite"
git remote add origin https://github.com/Alexsander13/api-tests-ganttpro.git
git branch -M main
git push -u origin main
```

### Subsequent Pushes
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

## Dependencies

- requests - HTTP client for API calls
- pytest - Test framework
- allure-pytest - Allure test reporting
- pytest-cov - Coverage reporting
- pytest-html - HTML reporting

See requirements.txt for all dependencies and versions.

## Documentation

- INSTRUCTIONS.md - Detailed test documentation and patterns
- src/navigation/TEST_INDEX.md - Complete test index
- api_spec.json - GanttPRO API details

## License

MIT License - Feel free to use this project for testing GanttPRO API

## Support

### Getting Help
1. Check INSTRUCTIONS.md for detailed test documentation
2. Review existing tests for patterns and examples
3. Check [GitHub Issues](https://github.com/Alexsander13/api-tests-ganttpro/issues)
4. Review test output and logs for error details

### Reporting Issues
1. Go to Issues tab in GitHub
2. Click New Issue
3. Describe the problem with:
   - What you were trying to do
   - What happened
   - Expected behavior
   - Test output/error message
   - Your environment (Python version, OS)

## Credits

GanttPRO API Test Suite - Created for automated testing of GanttPRO v1.0 API
