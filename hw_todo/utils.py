import requests
import os
import dotenv
from datetime import datetime

dotenv.load_dotenv()
CANVAS_TOKEN = os.environ['CANVAS_TOKEN']

BASE_URL = "https://canvas.instructure.com/api/v1/courses"


def get_courses():
    """Returns list of courses"""
    course_list = requests.get(
        BASE_URL, params={'access_token': CANVAS_TOKEN, 'enrollment_state': 'active'})
    return course_list.json()


def get_canvas_tasks():
    tasks = []

    courses = get_courses()

    for course in courses:
        course_id = course.get('id')

        response = requests.get('{}/{}/assignments'.format(BASE_URL, course_id), params={'access_token' : CANVAS_TOKEN, 'bucket' : 'upcoming'})
        assignments = response.json()
        course_name = ' '.join(course.get('name').split()) #substitute multiple whitespaces with one


        for assignment in assignments:
            assignment_id = assignment.get('id')
            assignment_name = assignment.get('name')
            due_date = datetime.strptime(assignment.get('due_at'), '%Y-%m-%dT%H:%M:%SZ')
            # description = assignment.get('description') #TODO: Use this later to show client description of assignments
            # html_url = assignment.get('html_url') # TODO: Use this later to give client a clickeable link to the assignment page

            tasks.append({
                "canvas_id": assignment_id,
                "assignment": assignment_name,
                "due_date": due_date,
                "course": course_name
                })
    return tasks