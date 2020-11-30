from hw_todo.tests import app, database


def test_default_url_post_returns_tasks():
    app.config['TESTING'] = True
    client = app.test_client()

    data = {"assignment": "orbit",
            "due_date": "2017-11-12T12:12",
            "course": "Graphics"}

    response = client.post('/', data=data)
    assert response.status_code == 200
    assert response.get_json() == {'Assignment': 'orbit',
                                   'Completed': False,
                                   'Course': 'Graphics',
                                   'Due Date': 'Sun, 12 Nov 2017 12:12:00 GMT',
                                   'Pending': True}


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

    response = client.get('/')
    assert response.status_code == 200
    expected = {'completedTasks': 0, 'pendingTasks': 0, 'tasks': []}
    assert response.get_json() == expected


def test_default_url_get_returns_tasks_after_tasks_added():
    app.config['TESTING'] = True
    client = app.test_client()

    data = {"assignment": "orbit",
            "due_date": "2017-11-12T12:12",
            "course": "Graphics"}

    client.post('/', data=data)
    response = client.get('/')
    assert response.status_code == 200
    expected = {'completedTasks': 0, 'pendingTasks': 1, 'tasks':
        [{'Assignment': 'orbit',
          'Completed': False,
          'Course': 'Graphics',
          'Due Date': 'Sun, 12 Nov 2017 12:12:00 GMT',
          'Pending': True}]}
    assert response.get_json() == expected


def test_canvas_returns_tasks():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/canvas')
    assert response.status_code == 200

    expected = {'Tasks': [{'Assignment': 'DB4',
                           'Canvas ID': 68020000000120216,
                           'Completed': False,
                           'Course': 'CSCI 265 A DATABASE SYSTEMS',
                           'Due Date': 'Tue, 01 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'DB5',
                           'Canvas ID': 68020000000120837,
                           'Completed': False,
                           'Course': 'CSCI 265 A DATABASE SYSTEMS',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Order Refactor',
                           'Canvas ID': 68020000000120693,
                           'Completed': False,
                           'Course': 'CSCI 295 2A ST:INTRODUCTION TO SOFTWARE TESTING',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'HW: Final Project',
                           'Canvas ID': 68020000000118854,
                           'Completed': False,
                           'Course': 'CSCI 298 A ST: WEB PROGRAMMING',
                           'Due Date': 'Mon, 30 Nov 2020 16:00:00 GMT',
                           'Pending': False},
                          {'Assignment': 'Quiz 12: Continuity and Change',
                           'Canvas ID': 68020000000121381,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Cherokee Removal',
                           'Canvas ID': 68020000000103601,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Continuity and Change',
                           'Canvas ID': 68020000000121387,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:00 GMT',
                           'Pending': False}]}
    assert response.get_json() == expected


def test_canvas_sets_tasks_to_complete_by_id():
    app.config['TESTING'] = True
    client = app.test_client()
    client.get('/canvas')
    response = client.put('/complete/68020000000121387')
    assert response.status_code == 200
    expected = {'Tasks': [{'Assignment': 'DB4',
                           'Canvas ID': 68020000000120216,
                           'Completed': False,
                           'Course': 'CSCI 265 A DATABASE SYSTEMS',
                           'Due Date': 'Tue, 01 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'DB5',
                           'Canvas ID': 68020000000120837,
                           'Completed': False,
                           'Course': 'CSCI 265 A DATABASE SYSTEMS',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Order Refactor',
                           'Canvas ID': 68020000000120693,
                           'Completed': False,
                           'Course': 'CSCI 295 2A ST:INTRODUCTION TO SOFTWARE TESTING',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'HW: Final Project',
                           'Canvas ID': 68020000000118854,
                           'Completed': False,
                           'Course': 'CSCI 298 A ST: WEB PROGRAMMING',
                           'Due Date': 'Mon, 30 Nov 2020 16:00:00 GMT',
                           'Pending': False},
                          {'Assignment': 'Quiz 12: Continuity and Change',
                           'Canvas ID': 68020000000121381,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Cherokee Removal',
                           'Canvas ID': 68020000000103601,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Continuity and Change',
                           'Canvas ID': 68020000000121387,
                           'Completed': True,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:00 GMT',
                           'Pending': False}]}
    assert response.get_json() == expected


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
    data = {"assignment": "Orbiting",
            "due_date": "2017-11-12T12:12",
            "course": "Graphics"}
    client.get('/canvas')
    response = client.post('/update/68020000000120216', data=data)
    assert response.status_code == 200
    expected = {'Tasks': [{'Assignment': 'Orbiting',
                           'Canvas ID': 68020000000120216,
                           'Completed': False,
                           'Course': 'Graphics',
                           'Due Date': 'Sun, 12 Nov 2017 12:12:00 GMT',
                           'Pending': False},
                          {'Assignment': 'DB5',
                           'Canvas ID': 68020000000120837,
                           'Completed': False,
                           'Course': 'CSCI 265 A DATABASE SYSTEMS',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Order Refactor',
                           'Canvas ID': 68020000000120693,
                           'Completed': False,
                           'Course': 'CSCI 295 2A ST:INTRODUCTION TO SOFTWARE TESTING',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'HW: Final Project',
                           'Canvas ID': 68020000000118854,
                           'Completed': False,
                           'Course': 'CSCI 298 A ST: WEB PROGRAMMING',
                           'Due Date': 'Mon, 30 Nov 2020 16:00:00 GMT',
                           'Pending': False},
                          {'Assignment': 'Quiz 12: Continuity and Change',
                           'Canvas ID': 68020000000121381,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Cherokee Removal',
                           'Canvas ID': 68020000000103601,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Continuity and Change',
                           'Canvas ID': 68020000000121387,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:00 GMT',
                           'Pending': False}]}
    assert response.get_json() == expected


def test_update_tasks_with_missing_value():
    app.config['TESTING'] = True
    client = app.test_client()
    data = {"assignment": "Orbiting",
            "course": "Graphics"}
    client.get('/canvas')
    response = client.post('/update/68020000000120216', data=data)
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
    client.get('/canvas')
    response = client.delete('/68020000000120216')
    assert response.status_code == 200
    expected = {'Tasks': [{'Assignment': 'DB5',
                           'Canvas ID': 68020000000120837,
                           'Completed': False,
                           'Course': 'CSCI 265 A DATABASE SYSTEMS',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Order Refactor',
                           'Canvas ID': 68020000000120693,
                           'Completed': False,
                           'Course': 'CSCI 295 2A ST:INTRODUCTION TO SOFTWARE TESTING',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'HW: Final Project',
                           'Canvas ID': 68020000000118854,
                           'Completed': False,
                           'Course': 'CSCI 298 A ST: WEB PROGRAMMING',
                           'Due Date': 'Mon, 30 Nov 2020 16:00:00 GMT',
                           'Pending': False},
                          {'Assignment': 'Quiz 12: Continuity and Change',
                           'Canvas ID': 68020000000121381,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Cherokee Removal',
                           'Canvas ID': 68020000000103601,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Wed, 02 Dec 2020 04:59:59 GMT',
                           'Pending': False},
                          {'Assignment': 'Continuity and Change',
                           'Canvas ID': 68020000000121387,
                           'Completed': False,
                           'Course': 'HIST 195 A ST: NATIVE NORTH AMERICA',
                           'Due Date': 'Sat, 05 Dec 2020 04:59:00 GMT',
                           'Pending': False}]}
    assert response.get_json() == expected


def test_delete_tasks_with_invalid_id():
    app.config['TESTING'] = True
    client = app.test_client()
    client.get('/canvas')
    response = client.delete('/20')
    assert response.status_code == 200
    expected = {'ERROR': 'ID Not Found'}
    assert response.get_json() == expected