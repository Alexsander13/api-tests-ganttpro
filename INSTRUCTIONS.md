# Instructions

## Setup

### Prerequisites
* Python 3.12 or higher
* pip (Python package manager)

### Installation

1. **Clone/navigate to project directory**
   ```bash
   cd api-tests-ganttpro
   ```

2. **Create and configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API_KEY and other credentials
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Run all tests
```bash
pytest
```

### Run smoke tests only
```bash
pytest tests/smoke/
```

### Run endpoints tests only
```bash
pytest tests/endpoints/
```

### Run scenarios tests only
```bash
pytest tests/scenarios/
```

### Run specific endpoint group
```bash
pytest tests/endpoints/tasks/
pytest tests/endpoints/comments/
pytest tests/endpoints/timelogs/
```

### Run with verbose output
```bash
pytest -v
```

### Run and generate reports (automatic)
Reports are generated automatically after each test run in `./reports/`:
* `report.html` - HTML test report
* `junit.xml` - JUnit XML report
* `coverage-html/` - Coverage report

### View coverage report
```bash
open reports/coverage-html/index.html  # macOS
```

## Regenerate Test Index

After adding new test files:
```bash
python src/navigation/generate_test_index.py
```

## Adding New Tests

### Adding a new endpoint test

1. **Identify the endpoint section** (tasks, comments, timelogs, etc.)
2. **Create test file** in `tests/endpoints/<section>/test_<section>_<operation>.py`
3. **Follow naming convention**: `test_<section>_<operation>.py`
4. **Add module docstring** at the top describing the test
5. **Use fixtures from conftest.py**: `client`, `auth_headers`, `task_id`, etc.
6. **Import assertions** from `src.assertions`
7. **Check IDs** and skip tests if required IDs are missing

Example:
```python
"""Test for updating a task via PUT /tasks/{taskId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys

def test_update_task_success(client, auth_headers, task_id):
    """Test successful task update returns 200"""
    if not task_id:
        pytest.skip("TASK_ID not configured in .env")
    
    payload = {"name": "Updated Task Name"}
    response = client.put(f"/tasks/{task_id}", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["status"])
```

### Adding a new scenario test

1. **Create test file** in `tests/scenarios/test_scenario_<name>.py`
2. **Add module docstring** describing the scenario
3. **Mark as `@pytest.mark.scenario`** for filtering
4. **Use multiple endpoints** in sequence to test realistic workflows

### Test organization rules

* One file per endpoint operation (GET, POST, PUT, DELETE)
* Group related endpoints in folders (tasks, comments, links, etc.)
* Always add module docstring for test index generation
* Use descriptive test function names
* Skip tests gracefully when required IDs are missing

## Environment Configuration

### Required variables
* `BASE_URL` - API base URL (default: https://api.ganttpro.com/v1.0)
* `API_KEY` - Your GanttPRO API key

### Optional ID variables
Tests will skip if these are not provided:
* `TASK_ID` - Valid task ID for task operations
* `PROJECT_ID` - Valid project ID for project queries
* `COMMENT_ID` - Valid comment ID for comment operations
* `TIMELOG_ID` - Valid time log ID
* `LINK_ID` - Valid link ID
* `ATTACHMENT_ID` - Valid attachment ID
* `RESOURCE_ID` - Valid resource ID
* `USER_ID` - Valid user ID

### Setting up test data

1. Create test resources in your GanttPRO account
2. Note the IDs of tasks, projects, etc.
3. Add IDs to `.env` file
4. Run tests to verify

## Test Markers

* `@pytest.mark.smoke` - Smoke tests
* `@pytest.mark.scenario` - Scenario tests
* Tests skip automatically when required IDs are missing

## Troubleshooting

### Tests are skipping
* Check `.env` file has required variables set
* Verify API_KEY is valid
* Ensure ID variables point to existing resources

### 401 Unauthorized errors
* Verify API_KEY in `.env` is correct
* Check API key has not expired

### 404 Not Found errors
* Verify IDs in `.env` point to existing resources
* Check resource has not been deleted

### Import errors
* Ensure dependencies are installed: `pip install -r requirements.txt`
* Check Python version: `python --version` (should be 3.12+)

## Project Maintenance

### Update API spec
1. Replace `api_spec.json` with new version
2. Add new endpoint tests as needed
3. Regenerate test index

### Update dependencies
```bash
pip install --upgrade -r requirements.txt
```

## Best Practices

* Keep `.env` file private (never commit)
* Use test IDs from a dedicated test account
* Run smoke tests before full suite
* Review HTML report after each run
* Update test index after adding tests
* Add module docstrings to all test files
* Use meaningful test function names
* Add comments for complex test logic
