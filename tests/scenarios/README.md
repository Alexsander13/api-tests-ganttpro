# Scenario Tests

Scenario tests are end-to-end integration tests that combine multiple API endpoints to test realistic workflows.

## Status: Placeholder (2nd Iteration)

This directory is reserved for scenario tests that will be implemented in the second iteration of this test suite.

## Planned Scenarios

* Task lifecycle: Create task → Assign resources → Add comments → Log time → Complete task
* Project setup: Create project → Add tasks → Link tasks → Assign team members
* Reporting workflow: Create tasks → Log time → Generate reports
* Collaboration: Multiple users adding comments and attachments to tasks

## How to Add Scenario Tests

1. Create a new file: `test_scenario_<name>.py`
2. Add module docstring describing the scenario
3. Mark tests with `@pytest.mark.scenario`
4. Use multiple endpoints in sequence to simulate user workflow
5. Add assertions at each step to verify state

## Example Structure

```python
"""Test scenario for task lifecycle workflow"""
import pytest

@pytest.mark.scenario
def test_complete_task_lifecycle(client, auth_headers):
    # Step 1: Create task
    # Step 2: Assign resources
    # Step 3: Add comment
    # Step 4: Log time
    # Step 5: Mark complete
    pass
```
