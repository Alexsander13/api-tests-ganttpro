"""Pytest configuration and shared fixtures.

Provides fixtures for HTTP client, authentication, and test data IDs.
"""
import os
import time
import pytest
from src.http_client import HTTPClient
from src.config import Config


@pytest.fixture(scope="session")
def client():
    """Create HTTP client instance.
    
    Returns:
        HTTPClient instance configured with base URL.
    """
    client = HTTPClient(base_url=Config.BASE_URL)
    # Store client globally for report access
    return client


@pytest.fixture(scope="session")
def auth_headers():
    """Get authentication headers.
    
    Returns:
        Dictionary with X-API-Key header.
    """
    return Config.get_auth_headers()


@pytest.fixture(scope="session")
def project_id():
    """Get project ID from environment.
    
    Skips test if PROJECT_ID is not available.
    
    Returns:
        Project ID as string.
    """
    value = Config.PROJECT_ID
    if not value:
        pytest.skip("PROJECT_ID not available")
    return value


@pytest.fixture(scope="session")
def test_task_id(client, auth_headers, project_id):
    """Create a test task and return its ID.
    
    Returns:
        Task ID string.
    """
    if not project_id:
        pytest.skip("PROJECT_ID not available")
    
    # Create test task
    task_data = {
        "projectId": int(project_id),
        "name": "Test Task for API Testing",
        "description": "Automatically created for testing purposes"
    }
    
    response = client.post("/tasks", headers=auth_headers, json=task_data)
    if response.status_code in [200, 201]:
        # API returns response wrapped in 'item' key
        task_id = str(response.json().get('item', {}).get('id'))
        yield task_id
        # Cleanup: delete task after tests
        try:
            client.delete(f"/tasks/{task_id}", headers=auth_headers)
        except:
            pass  # Ignore cleanup errors
    else:
        pytest.skip(f"Could not create test task: {response.status_code}")


@pytest.fixture(scope="session")
def task_id(test_task_id):
    """Alias for test_task_id for backward compatibility.
    
    Returns:
        Task ID string.
    """
    return test_task_id


@pytest.fixture(scope="function")
def fresh_task_id(client, auth_headers, project_id):
    """Create a task for a single test and clean it up."""
    if not project_id:
        pytest.skip("PROJECT_ID not available")

    task_data = {
        "projectId": int(project_id),
        "name": "Temp Task for test",
        "description": "Created per-test for isolation"
    }

    response = client.post("/tasks", headers=auth_headers, json=task_data)
    if response.status_code not in [200, 201]:
        pytest.skip(f"Could not create per-test task: {response.status_code}")

    created_id = str(response.json().get("item", {}).get("id"))
    yield created_id

    try:
        client.delete(f"/tasks/{created_id}", headers=auth_headers)
    except Exception:
        pass


@pytest.fixture(scope="session")
def comment_id(client, auth_headers, test_task_id):
    """Create a test comment and return its ID.
    
    Returns:
        Comment ID string.
    """
    if not test_task_id:
        pytest.skip("TASK_ID not available")
    
    # Create test comment
    comment_data = {
        "taskId": int(test_task_id),
        "content": "Test comment for API testing"
    }
    
    response = client.post("/comments", headers=auth_headers, json=comment_data)
    if response.status_code in [200, 201]:
        comment_id = str(response.json().get('item', {}).get('id'))
        yield comment_id
        # Cleanup: delete comment after tests
        try:
            client.delete(f"/comments/{comment_id}", headers=auth_headers)
        except:
            pass
    else:
        pytest.skip(f"Could not create test comment: {response.status_code}")


@pytest.fixture(scope="session")
def timelog_id(client, auth_headers, test_task_id, resource_id):
    """Create a test timelog and return its ID.
    
    Returns:
        Timelog ID string.
    """
    if not test_task_id or not resource_id:
        pytest.skip("TASK_ID or RESOURCE_ID not available")
    
    # Create test timelog
    timelog_data = {
        "taskId": int(test_task_id),
        "resourceId": int(resource_id),
        "date": "2024-01-15",
        "time": 4.0,
        "description": "Test timelog for API testing"
    }
    
    response = client.post("/timeLogs", headers=auth_headers, json=timelog_data)
    if response.status_code in [200, 201]:
        # API returns id at top level, not wrapped in 'item'
        timelog_id = str(response.json().get('id'))
        yield timelog_id
        # Cleanup: delete timelog after tests
        try:
            client.delete(f"/timeLogs/{timelog_id}", headers=auth_headers)
        except:
            pass
    else:
        pytest.skip(f"Could not create test timelog: {response.status_code}")


@pytest.fixture(scope="session")
def link_id(client, auth_headers, project_id, test_task_id):
    """Create a test link and return its ID.
    
    Returns:
        Link ID string.
    """
    if not project_id or not test_task_id:
        pytest.skip("PROJECT_ID or TASK_ID not available")
    
    # Create second task for linking
    task_data = {
        "projectId": int(project_id),
        "name": "Second Test Task for Link",
        "description": "Target task for link testing"
    }
    
    response = client.post("/tasks", headers=auth_headers, json=task_data)
    if response.status_code not in [200, 201]:
        pytest.skip(f"Could not create second task: {response.status_code}")
    
    task2_id = str(response.json().get('item', {}).get('id'))
    
    # Create link between tasks
    link_data = {
        "projectId": int(project_id),
        "source": int(test_task_id),
        "target": int(task2_id),
        "type": 0  # finish-to-start
    }
    
    response = client.post("/links", headers=auth_headers, json=link_data)
    if response.status_code in [200, 201]:
        # API returns id at top level, not wrapped in 'item'
        link_id = str(response.json().get('id'))
        yield link_id
        # Cleanup: delete link and second task
        try:
            client.delete(f"/links/{link_id}", headers=auth_headers)
            client.delete(f"/tasks/{task2_id}", headers=auth_headers)
        except:
            pass
    else:
        pytest.skip(f"Could not create test link: {response.status_code}")


@pytest.fixture(scope="session")
def attachment_id():
    """Attachment ID fixture - skip as file upload is complex.
    
    Returns:
        None (always skips).
    """
    pytest.skip("Attachment tests require file upload which is not yet implemented")


@pytest.fixture(scope="session")
def resource_id():
    """Get resource ID from environment.
    
    Skips test if RESOURCE_ID is not available.
    
    Returns:
        Resource ID as string.
    """
    value = Config.RESOURCE_ID
    if not value:
        pytest.skip("RESOURCE_ID not available")
    return value


@pytest.fixture(scope="session")
def user_id():
    """Get user ID from environment.
    
    Skips test if USER_ID is not available.
    
    Returns:
        User ID as string.
    """
    value = Config.USER_ID
    if not value:
        pytest.skip("USER_ID not available")
    return value


@pytest.fixture(scope="session", autouse=True)
def setup_reports_dir():
    """Create reports directory if it doesn't exist."""
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(os.path.join(reports_dir, "coverage-html"), exist_ok=True)


@pytest.fixture(autouse=True)
def rate_limit_pause():
    """Add pause between tests to avoid API rate limiting."""
    yield
    # Pause after each test (1 second to be safe)
    time.sleep(1)


# HTML Report customization
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add custom information to test report."""
    outcome = yield
    report = outcome.get_result()
    
    # Add extra info to report
    if report.when == 'call':
        # Get test docstring as description
        if item.function.__doc__:
            report.description = item.function.__doc__.strip()
        
        # Capture HTTP client request history if available
        if 'client' in item.funcargs:
            client = item.funcargs['client']
            if hasattr(client, 'request_history') and client.request_history:
                report.request_info = client.request_history[-1]
            else:
                report.request_info = None
        else:
            report.request_info = None


def pytest_html_results_table_header(cells):
    """Customize HTML report table headers."""
    cells.insert(2, '<th class="sortable" style="min-width: 300px;">Endpoint</th>')
    cells.insert(3, '<th class="sortable" style="min-width: 80px;">Method</th>')
    cells.insert(4, '<th style="min-width: 400px;">Request</th>')
    cells.insert(5, '<th style="min-width: 400px;">Response</th>')


def pytest_html_results_table_row(report, cells):
    """Customize HTML report table rows."""
    import json
    
    # Extract endpoint and method from test name
    endpoint = ''
    method = ''
    description = getattr(report, 'description', '')
    
    # Try to get request info
    request_info = getattr(report, 'request_info', None)
    
    if request_info:
        endpoint = request_info.get('url', 'N/A')
        method = request_info.get('method', 'N/A')
        
        # Format request details
        request_body = request_info.get('body')
        request_params = request_info.get('params')
        
        request_parts = []
        if request_params:
            params_html = f'<div style="margin-top:8px;"><strong>Parameters:</strong></div><pre style="background:#f5f5f5;padding:8px;border-radius:4px;font-size:11px;margin:4px 0;">{json.dumps(request_params, indent=2)}</pre>'
            request_parts.append(params_html)
        
        if request_body:
            body_html = f'<div style="margin-top:8px;"><strong>Body:</strong></div><pre style="background:#f5f5f5;padding:8px;border-radius:4px;font-size:11px;margin:4px 0;">{json.dumps(request_body, indent=2)}</pre>'
            request_parts.append(body_html)
        
        if not request_parts:
            request_str = '<span style="color:#999;font-style:italic;">No request body</span>'
        else:
            request_str = ''.join(request_parts)
        
        # Format response details
        response = request_info.get('response', {})
        status_code = response.get('status_code', 'N/A')
        response_body = response.get('body', '')
        
        # Parse response if JSON
        try:
            if response_body:
                response_json = json.loads(response_body)
                response_formatted = json.dumps(response_json, indent=2)
            else:
                response_formatted = 'Empty response'
        except:
            response_formatted = response_body[:500] if response_body else 'Empty response'
        
        # Color code status
        if isinstance(status_code, int):
            if 200 <= status_code < 300:
                status_color = '#28a745'
                status_bg = '#d4edda'
            elif 400 <= status_code < 500:
                status_color = '#fd7e14'
                status_bg = '#fff3cd'
            elif 500 <= status_code < 600:
                status_color = '#dc3545'
                status_bg = '#f8d7da'
            else:
                status_color = '#6c757d'
                status_bg = '#e9ecef'
        else:
            status_color = '#6c757d'
            status_bg = '#e9ecef'
        
        response_str = f'''
        <div style="background:{status_bg};border-left:4px solid {status_color};padding:8px;margin:4px 0;border-radius:4px;">
            <strong style="color:{status_color};font-size:13px;">Status: {status_code}</strong>
        </div>
        <pre style="background:#f5f5f5;padding:8px;border-radius:4px;font-size:11px;margin:4px 0;max-height:300px;overflow:auto;">{response_formatted}</pre>
        '''
        
        # Method badge styling
        method_colors = {
            'GET': '#0d6efd',
            'POST': '#198754',
            'PUT': '#ffc107',
            'DELETE': '#dc3545'
        }
        method_color = method_colors.get(method, '#6c757d')
        method_badge = f'<span style="background:{method_color};color:white;padding:4px 12px;border-radius:4px;font-weight:bold;font-size:11px;display:inline-block;">{method}</span>'
        
        cells.insert(2, f'<td style="font-size:11px;word-break:break-word;"><code style="background:#f8f9fa;padding:2px 6px;border-radius:3px;">{endpoint}</code></td>')
        cells.insert(3, f'<td style="text-align:center;">{method_badge}</td>')
        cells.insert(4, f'<td style="font-size:11px;">{request_str}</td>')
        cells.insert(5, f'<td style="font-size:11px;">{response_str}</td>')
    else:
        # Fallback to parsing from test name
        if hasattr(report, 'nodeid'):
            # Parse test path to extract endpoint info
            if '/endpoints/' in report.nodeid:
                parts = report.nodeid.split('/')
                for i, part in enumerate(parts):
                    if part == 'endpoints' and i + 1 < len(parts):
                        endpoint = parts[i + 1]
                        break
            elif '/smoke/' in report.nodeid:
                endpoint = 'smoke'
            elif '/scenarios/' in report.nodeid:
                endpoint = 'scenarios'
            
            # Extract method from test name
            test_name = report.nodeid.split('::')[-1] if '::' in report.nodeid else ''
            if 'get' in test_name.lower():
                method = 'GET'
            elif 'post' in test_name.lower() or 'add' in test_name.lower() or 'create' in test_name.lower():
                method = 'POST'
            elif 'put' in test_name.lower() or 'update' in test_name.lower():
                method = 'PUT'
            elif 'delete' in test_name.lower():
                method = 'DELETE'
        
        cells.insert(2, f'<td style="color:#999;">{endpoint if endpoint else "N/A"}</td>')
        cells.insert(3, f'<td style="color:#999;">{method if method else "N/A"}</td>')
        cells.insert(4, f'<td style="color:#999;font-style:italic;">No request data</td>')
        cells.insert(5, f'<td style="color:#999;font-style:italic;">No response data</td>')

