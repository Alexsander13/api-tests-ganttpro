# Test Index

Auto-generated index of all test files in the GanttPRO API test suite.

## Smoke Tests

* [test_smoke_public_gets](tests/smoke/test_smoke_public_gets.py) - Smoke tests for public GET endpoints and authentication.

## Endpoint Tests

### Attachments

* [test_attachments_add](tests/endpoints/attachments/test_attachments_add.py) - Test for adding attachment via POST /attachments
* [test_attachments_delete](tests/endpoints/attachments/test_attachments_delete.py) - Test for deleting attachment via DELETE /attachments/{attachmentId}
* [test_attachments_delete_by_ids](tests/endpoints/attachments/test_attachments_delete_by_ids.py) - Test for deleting attachments by IDs via DELETE /attachments/delete/byIds
* [test_attachments_get_by_project](tests/endpoints/attachments/test_attachments_get_by_project.py) - Test for getting attachments by project ID via GET /attachments/getByProjectId
* [test_attachments_get_list](tests/endpoints/attachments/test_attachments_get_list.py) - Test for getting attachments list via GET /attachments

### Colors

* [test_colors_get](tests/endpoints/colors/test_colors_get.py) - Test for getting colors via GET /colors

### Comments

* [test_comments_add](tests/endpoints/comments/test_comments_add.py) - Test for adding a comment via POST /comments
* [test_comments_delete](tests/endpoints/comments/test_comments_delete.py) - Test for deleting a comment via DELETE /comments/{commentId}
* [test_comments_get_by_project](tests/endpoints/comments/test_comments_get_by_project.py) - Test for getting comments by project ID via GET /comments/getByProjectId
* [test_comments_get_list](tests/endpoints/comments/test_comments_get_list.py) - Test for getting comments list via GET /comments
* [test_comments_update](tests/endpoints/comments/test_comments_update.py) - Test for updating a comment via PUT /comments/{commentId}

### Languages

* [test_languages_get](tests/endpoints/languages/test_languages_get.py) - Test for getting languages via GET /languages

### Links

* [test_links_create](tests/endpoints/links/test_links_create.py) - Test for creating a link via POST /links
* [test_links_delete](tests/endpoints/links/test_links_delete.py) - Test for deleting a link via DELETE /links/{linkId}
* [test_links_get](tests/endpoints/links/test_links_get.py) - Test for getting a link via GET /links/{linkId}
* [test_links_update](tests/endpoints/links/test_links_update.py) - Test for updating a link via PUT /links/{linkId}

### Resources

* [test_resources_get_list](tests/endpoints/resources/test_resources_get_list.py) - Test for getting resources list via GET /resources

### Roles

* [test_roles_account_get](tests/endpoints/roles/test_roles_account_get.py) - Test for getting account roles via GET /roles/account
* [test_roles_project_get](tests/endpoints/roles/test_roles_project_get.py) - Test for getting project roles via GET /roles/project

### Tasks

* [test_tasks_assign_resource_delete](tests/endpoints/tasks/test_tasks_assign_resource_delete.py) - Test for deleting resource assignment via DELETE /tasks/{taskId}/assignResource
* [test_tasks_assign_resource_post](tests/endpoints/tasks/test_tasks_assign_resource_post.py) - Test for assigning resources to task via POST /tasks/{taskId}/assignResource
* [test_tasks_assign_resource_put](tests/endpoints/tasks/test_tasks_assign_resource_put.py) - Test for updating task resources via PUT /tasks/{taskId}/assignResource
* [test_tasks_delete_task](tests/endpoints/tasks/test_tasks_delete_task.py) - Test for deleting a task via DELETE /tasks/{taskId}
* [test_tasks_update_task](tests/endpoints/tasks/test_tasks_update_task.py) - Test for updating a task via PUT /tasks/{taskId}

### Timelogs

* [test_timelogs_add](tests/endpoints/timelogs/test_timelogs_add.py) - Test for adding a time log via POST /timeLogs
* [test_timelogs_delete](tests/endpoints/timelogs/test_timelogs_delete.py) - Test for deleting a time log via DELETE /timeLogs/{timeLogId}
* [test_timelogs_get_by_project](tests/endpoints/timelogs/test_timelogs_get_by_project.py) - Test for getting time logs by project ID via GET /timeLogs/getByProjectId
* [test_timelogs_get_list](tests/endpoints/timelogs/test_timelogs_get_list.py) - Test for getting time logs list via GET /timeLogs
* [test_timelogs_get_one](tests/endpoints/timelogs/test_timelogs_get_one.py) - Test for getting a time log via GET /timeLogs/{timeLogId}
* [test_timelogs_update](tests/endpoints/timelogs/test_timelogs_update.py) - Test for updating a time log via PUT /timeLogs/{timeLogId}

## Scenario Tests

* [test_scenario_example](tests/scenarios/test_scenario_example.py) - Minimal placeholder scenario test, skipped by default

*This index is automatically generated. Run `python src/navigation/generate_test_index.py` to update.*
