from hw_todo.tests import app
from datetime import datetime


''' Set your Canvas Token in utils.py before you run the tests'''


def test_canvas_returns_tasks():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/canvas')
    assert response.status_code == 200


def test_canvas_sets_tasks_to_complete_by_id():
    app.config['TESTING'] = True
    client = app.test_client()
    database = client.get('/canvas').get_json()
    response = client.put('/complete/' + str(database["Tasks"][0]["Canvas ID"]))
    assert response.status_code == 200
    database["Tasks"][0]["Completed"] = True
    assert response.get_json() == database


def test_canvas_sets_tasks_to_complete_by_invalid_id():
    app.config['TESTING'] = True
    client = app.test_client()
    client.get('/canvas')
    response = client.put('/complete/40')
    assert response.status_code == 200
    expected = {'ERROR': 'ID Not Found'}
    assert response.get_json() == expected


def test_update_tasks_with_three_values():
    app.config['TESTING'] = True
    client = app.test_client()
    database = client.get('/canvas').get_json()

    data = {"assignment": "Orbiting",
            "due_date": "2017-11-12T12:12",
            "course": "Graphics"}
    response = client.post('/update/' + str(database["Tasks"][0]["Canvas ID"]), data=data)
    assert response.status_code == 200
    database["Tasks"][0]["Assignment"] = "Orbiting"
    database["Tasks"][0]["Due Date"] = 'Sun, 12 Nov 2017 12:12:00 GMT'
    database["Tasks"][0]["Course"] = "Graphics"
    assert response.get_json() == database


def test_update_tasks_with_missing_value():
    app.config['TESTING'] = True
    client = app.test_client()
    database = client.get('/canvas').get_json()
    data = {"assignment": "Orbiting",
            "course": "Graphics"}
    client.get('/canvas')
    response = client.post('/update/' + str(database["Tasks"][0]["Canvas ID"]), data=data)
    assert response.status_code == 200
    expected = {"ERROR": "MISSING INFORMATION"}
    assert response.get_json() == expected


def test_update_tasks_with_invalid_id():
    app.config['TESTING'] = True
    client = app.test_client()
    data = {"assignment": "Orbiting",
            "course": "Graphics"}
    client.get('/canvas')
    response = client.post('/update/20', data=data)
    assert response.status_code == 200
    expected = {'ERROR': 'ID Not Found'}
    assert response.get_json() == expected


def test_delete_task():
    app.config['TESTING'] = True
    client = app.test_client()
    database = client.get('/canvas').get_json()

    data = {"assignment": "Orbiting",
            "due_date": "2017-11-12T12:12",
            "course": "Graphics"}
    response = client.delete('/' + str(database["Tasks"][0]["Canvas ID"]), data=data)
    assert response.status_code == 200
    database["Tasks"].pop(0)
    assert response.get_json() == database


def test_delete_tasks_with_invalid_id():
    app.config['TESTING'] = True
    client = app.test_client()
    client.get('/canvas')
    response = client.delete('/20')
    assert response.status_code == 200
    expected = {'ERROR': 'ID Not Found'}
    assert response.get_json() == expected


def test_default_url_post_returns_tasks():
    app.config['TESTING'] = True
    client = app.test_client()
    database = client.get('/canvas').get_json()
    data = {"assignment": "orbit",
            "due_date": "2017-11-12T12:12",
            "course": "Graphics"}
    response = client.post('/', data=data)
    assert response.status_code == 200
    data["due_date"] = 'Sun, 12 Nov 2017 12:12:00 GMT'
    database["Tasks"].append(data)
    assert response.get_json() == database



def test_default_url_post_returns_error_if_assignment_missing():
    app.config['TESTING'] = True
    client = app.test_client()

    data = {"due_date": "2017-11-12T12:12",
            "course": "Graphics"}

    response = client.post('/', data=data)
    assert response.status_code == 400
    expected = {'error': 'assignment, due_date and course required as form data'}
    assert response.get_json() == expected


def test_default_url_post_returns_error_if_due_date_missing():
    app.config['TESTING'] = True
    client = app.test_client()

    data = {"assignment": "orbit",
            "course": "Graphics"}

    response = client.post('/', data=data)
    assert response.status_code == 400
    expected = {'error': 'assignment, due_date and course required as form data'}
    assert response.get_json() == expected


def test_default_url_post_returns_error_if_course_missing():
    app.config['TESTING'] = True
    client = app.test_client()

    data = {"assignment": "orbit",
            "due_date": "2017-11-12T12:12"}

    response = client.post('/', data=data)
    assert response.status_code == 400
    expected = {'error': 'assignment, due_date and course required as form data'}
    assert response.get_json() == expected


def test_default_url_post_returns_error_if_no_data_passed():
    app.config['TESTING'] = True
    client = app.test_client()

    data = {}

    response = client.post('/', data=data)
    assert response.status_code == 400
    expected = {'error': 'assignment, due_date and course required as form data'}
    assert response.get_json() == expected


def test_default_url_get_returns_zero_tasks():
    app.config['TESTING'] = True
    client = app.test_client()
    database = client.get('/canvas').get_json()

    response = client.get('/')
    assert response.status_code == 200
    expected = {'completedTasks': 0, 'pendingTasks': 0, 'tasks': database["Tasks"]}
    assert response.get_json() == expected


def test_default_url_get_returns_tasks_after_tasks_added():
    app.config['TESTING'] = True
    client = app.test_client()
    database = client.get('/canvas').get_json()
    data = {"assignment": "orbit",
            "due_date": "2017-11-12T12:12",
            "course": "Graphics"}
    response = client.post('/', data=data)
    assert response.status_code == 200
    data["due_date"] = 'Sun, 12 Nov 2017 12:12:00 GMT'
    database["Tasks"].append(data)
    response = client.get('/')
    assert response.status_code == 200
    expected = {'completedTasks': 0, 'pendingTasks': 0, 'tasks': database["Tasks"]}
    assert response.get_json() == expected
