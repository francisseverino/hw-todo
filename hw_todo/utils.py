import requests
import os
import dotenv
from twilio.rest import Client
from datetime import datetime
from hw_todo import app, db
from hw_todo.models import Todo

dotenv.load_dotenv()
CANVAS_TOKEN = os.environ['CANVAS_TOKEN']

BASE_URL = "https://canvas.instructure.com/api/v1/courses"


def send_sms():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    service_sid = os.environ['TWILIO_MESSAGE_SID']
    phone_number = os.environ['TWILIO_PHONE_NUMBER'] #TODO: Make it so user gets prompted to write their own phone
    client = Client(account_sid, auth_token)

    tasks = Todo.query.all()

    message = client.messages \
        .create(
            messaging_service_sid=service_sid,
            body=tasks,
            to=phone_number
        )

    print(message.sid)

def check_if_exists(canvas_id):
    """
    Helper Method
    Checks if a given canvas assignment already exists in the db
    :return: Boolean (True if exists in db, False if not)
    """
    existing_tasks = Todo.query.all()
    for task in existing_tasks:
        if task.canvas_id == canvas_id:
            return task.id
    return -1

def get_courses():
    """
    Returns list of active courses in Canvas LMS for given user's token
    :return: List of courses
    """
    course_list = requests.get(
        BASE_URL, params={'access_token': CANVAS_TOKEN, 'enrollment_state': 'active'})
    return course_list.json()


def get_canvas_tasks():
    """
    Returns a list of upcoming assignments in Canvas LMS for given user's token
    :return: List of objects {canvas_id, assignment, due_Date, course}
    """
    # ? Maybe call another endpoint because some professors don't have assignments page
    tasks = []

    courses = get_courses()

    for course in courses:
        course_id = course.get('id')

        response = requests.get('{}/{}/assignments'.format(BASE_URL, course_id),
                                params={'access_token': CANVAS_TOKEN, 'bucket': 'upcoming'})
        assignments = response.json()
        # substitute multiple whitespaces with one
        course_name = ' '.join(course.get('name').split())

        for assignment in assignments:
            assignment_id = assignment.get('id')
            assignment_name = assignment.get('name')
            due_date = datetime.strptime(
                assignment.get('due_at'), '%Y-%m-%dT%H:%M:%SZ')
            # description = assignment.get('description') #TODO: Use this later to show client description of assignments
            html_url = assignment.get('html_url').replace("/canvas.", "/moravian.")
            
            if_exists_id = check_if_exists(assignment_id)
            if (if_exists_id == -1):
                new_task = Todo(assignment=assignment_name, due_date=due_date, course=course_name, canvas_id=assignment_id, html_url = html_url)
                try:
                    db.session.add(new_task)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    return 'There was an issue pulling your tasks from canvas'
            else:
                task = Todo.query.get_or_404(if_exists_id)
                task.assignment = assignment_name
                task.due_date = due_date
                task.course = course_name
                task.html_url = html_url
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    return 'There was an issue pulling your tasks from canvas'
                
    return tasks