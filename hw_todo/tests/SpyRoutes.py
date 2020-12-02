from flask import render_template, request, jsonify
from datetime import datetime
from hw_todo.utils import get_canvas_tasks
from hw_todo.tests import app

db_canvas = {"Tasks": []}
db = db_canvas


@app.route('/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    (GET, POST)
    GET -> Homepage, returns list of tasks
    POST -> Add a new task to the database
    """
    if request.method == 'POST':
        if 'assignment' not in request.form or 'due_date' not in request.form or 'course' not in request.form:
            return jsonify(({'error': 'assignment, due_date and course required as form data'})), 400
        assignment = request.form['assignment']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
        course = request.form['course']


        try:
            # database.session.add(new_task)
            # database.session.commit()
            db["Tasks"].append({"assignment": assignment,
                                "due_date": due_date,
                                "course": course})

            return db
        except Exception as e:
            print(e)
            return 'There was an issue adding your task'

    else:
        # tasks = Todo.query.order_by(Todo.due_date).all()  # Orders by due date
        # completedTasks = len(list(filter(lambda x: x.completed, tasks)))
        # pendingTasks = len(tasks) - completedTasks
        tasks = db["Tasks"]
        completedTasks = 0
        pendingTasks = 0

        try:
            for x in range(len(tasks)):
                if tasks[x]["Completed"]:
                    completedTasks += 1
                if tasks[x]["Pending"]:
                    pendingTasks += 1

            return {"tasks": tasks, "completedTasks": completedTasks, "pendingTasks": pendingTasks}
        except KeyError:
            return {"tasks": tasks, "completedTasks": completedTasks, "pendingTasks": pendingTasks}


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    """
    (POST)
    Updates any field of the given assignment
    """
    existing_tasks = db_canvas["Tasks"]
    task_to_update = {}
    for x in range(len(db_canvas["Tasks"])):
        if existing_tasks[x]["Canvas ID"] == id:
            task_to_update = existing_tasks[x]

    if task_to_update == {}:
        return {"ERROR": "ID Not Found"}

    try:
        task_to_update["Assignment"] = request.form['assignment']
        task_to_update["Due Date"] = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
        task_to_update["Course"] = request.form['course']
    except Exception as e:
        print(e)
        return {"ERROR": "MISSING INFORMATION"}

    try:
        # database.session.commit()
        return db_canvas
    except Exception as e:
        print(e)
        return 'There was an issue updating your task'


@app.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    (DELETE)
    Deletes the given assignment
    """
    existing_tasks = db_canvas["Tasks"]
    task_location = ""
    task_to_delete = {}
    for x in range(len(db_canvas["Tasks"])):
        if existing_tasks[x]["Canvas ID"] == id:
            task_location = x
            task_to_delete = existing_tasks[x]

    if task_to_delete == {}:
        return {"ERROR": "ID Not Found"}

    try:
        db_canvas["Tasks"].pop(task_location)
        return db_canvas
    except:
        return 'There was a problem deleting that task'


def check_if_exists(canvas_id):
    """
    Helper Method
    Checks if a given canvas assignment already exists in the database
    :return: Boolean (True if exists in database, False if not)
    """
    existing_tasks = db_canvas["Tasks"]
    for x in range(len(db_canvas["Tasks"])):
        if existing_tasks[x]["Canvas ID"] == canvas_id:
            return True
    return False


@app.route('/canvas')
def canvas():
    """
    (GET)
    Updates the database with all new assignments from Canvas LMS 
    """
    tasks = get_canvas_tasks()
    for task in tasks:
        if not check_if_exists(task['canvas_id']):

            try:
                # new_task = Todo(assignment=task['assignment'], due_date=task['due_date'], course=task['course'],
                #                 canvas_id=task['canvas_id'])

                db_canvas["Tasks"].append({
                    "Assignment": task['assignment'],
                    "Due Date": task['due_date'],
                    "Course": task['course'],
                    "Canvas ID": task['canvas_id'],
                    "Completed": False,
                    "Pending": False
                })
            except Exception as e:
                print(e)
                return 'There was an issue pulling your tasks from canvas'

    return db_canvas


@app.route('/complete/<int:id>', methods=['PUT'])
def complete(id):
    """
    (GET)
    Updates the completed field of the given assignment to either True or False
    """

    existing_tasks = db_canvas["Tasks"]
    task_to_complete = {}
    for x in range(len(db_canvas["Tasks"])):
        if existing_tasks[x]["Canvas ID"] == id:
            task_to_complete = existing_tasks[x]

    if task_to_complete == {}:
        print("HIT")
        return {"ERROR": "ID Not Found"}

    try:
        task_to_complete["Completed"] = not task_to_complete["Completed"]
        # database.session.commit()
        return db_canvas, 200
    except Exception as e:
        print(e)
        return 'There was a problem completing that task'


