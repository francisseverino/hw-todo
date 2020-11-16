from hw_todo import app, db
from flask import render_template, url_for, request, redirect
from datetime import datetime
from hw_todo.models import Todo 


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
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
        return render_template('index.html', tasks=tasks)


@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete = Todo.query.get_or_404(id)
    

    try:
        task_to_complete.completed = not task_to_complete.completed
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return 'There was a problem completing that task'


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    task.due_date = task.due_date.strftime('%Y-%m-%dT%H:%M') # converts due date to string

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task, )


# if __name__ == "__main__":
#     app.run(debug=True)
