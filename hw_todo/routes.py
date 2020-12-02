from hw_todo import app, db
from flask import render_template, url_for, request, redirect, jsonify, Response
from datetime import datetime
from hw_todo.models import Todo 
from .utils import get_canvas_tasks


@app.route('/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    (GET, POST)
    GET -> Homepage, returns list of tasks
    POST -> Add a new task to the db
    """
    if request.method == 'POST':
        if 'assignment' not in request.form or 'due_date' not in request.form or 'course' not in request.form:
            return jsonify(({'error': 'assignment, due_date and course required as form data'})), 400
        assignment = request.form['assignment']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
        course = request.form['course']

        new_task = Todo(assignment=assignment, due_date=due_date, course=course)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.due_date).all() #Orders by due date
        completedTasks = len(list(filter(lambda x: x.completed, tasks)))
        pendingTasks = len(tasks) - completedTasks
        return render_template('index.html', tasks=tasks, completedTasks=completedTasks, pendingTasks=pendingTasks)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    """
    (POST)
    Updates any field of the given assignment
    """
    task = Todo.query.get_or_404(id)
    task.assignment = request.form['assignment']
    task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
    task.course = request.form['course']

    try:
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return 'There was an issue updating your task'


@app.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    (DELETE)
    Deletes the given assignment
    """
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return Response(status=204)
    except:
        return 'There was a problem deleting that task'


def check_if_exists(canvas_id):
    """
    Helper Method
    Checks if a given canvas assignment already exists in the db
    :return: Boolean (True if exists in db, False if not)
    """
    existing_tasks = Todo.query.all()
    for task in existing_tasks:
        if task.canvas_id == canvas_id:
            return True
    return False



@app.route('/canvas')
def canvas():
    """
    (GET)
    Updates the db with all new assignments from Canvas LMS 
    """
    tasks = get_canvas_tasks()
    for task in tasks:
        if not check_if_exists(task['canvas_id']):
            new_task = Todo(assignment=task['assignment'], due_date=task['due_date'], course=task['course'], canvas_id=task['canvas_id'])
            try:
                db.session.add(new_task)
                db.session.commit()
            except Exception as e:
                print(e)
                return 'There was an issue pulling your tasks from canvas'
    
    return redirect('/')


@app.route('/complete/<int:id>', methods=['PUT'])
def complete(id):
    """
    (GET)
    Updates the completed field of the given assignment to either True or False
    """
    task_to_complete = Todo.query.get_or_404(id)
    

    try:
        task_to_complete.completed = not task_to_complete.completed
        db.session.commit()
        return Response(status=204)
    except Exception as e:
        print(e)
        return 'There was a problem completing that task'
