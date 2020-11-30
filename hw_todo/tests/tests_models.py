from datetime import datetime
from hw_todo.tests import database


class Todo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    assignment = database.Column(database.String(200), nullable=False)
    date_created = database.Column(database.DateTime, default=datetime.utcnow)
    due_date = database.Column(database.DateTime, nullable=False)
    course = database.Column(database.String(200), nullable=False)
    completed = database.Column(database.Boolean, nullable=False, default=False)
    canvas_id = database.Column(database.Integer)

    def __repr__(self):
        return '<Task %r>' % self.id
