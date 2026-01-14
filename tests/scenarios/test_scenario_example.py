"""Minimal placeholder scenario test, skipped by default"""
import pytest


@pytest.mark.scenario
@pytest.mark.skip(reason="Scenario tests are placeholder for 2nd iteration")
def test_scenario_example(client, auth_headers):
    """Example scenario test - placeholder for future implementation"""
    # This is a placeholder for future scenario tests
    # Scenarios will combine multiple endpoints to test realistic workflows
    pass
