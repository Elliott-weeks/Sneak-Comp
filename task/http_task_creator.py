from google.cloud import tasks_v2
import datetime
import json
from footgasm.settings import production

def create_task(project:str, queue:str, location:str, payload:str,task_name:str, task_handler_relative_uri:str, in_seconds:int = None):

    client = tasks_v2.CloudTasksClient(credentials= production.GS_CREDENTIALS)

    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': tasks_v2.HttpMethod.POST,
                'relative_uri': task_handler_relative_uri
            }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["app_engine_http_request"]["headers"] = {"Content-type": "application/json"}
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task['app_engine_http_request']['body'] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        timestamp = datetime.datetime.now() + datetime.timedelta(seconds=in_seconds)

        # Add the timestamp to the tasks.
        task['schedule_time'] = timestamp
    if task_name is not None:
        # Add the name to tasks.
        task["name"] = task_name

    # Use the client to build and send the task.
    response = client.create_task(parent=parent, task=task)

    print('Created task {}'.format(response.name))
    return response
