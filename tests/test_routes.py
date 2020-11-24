from unittest import TestCase
from hw_todo import app, db
from hw_todo.models import Todo


class Test(TestCase):

    def test_server_returns_empty_list(self):
        # Create the Flask server using a new (empty) TodoList instance
        app.config['TESTING'] = True
        client = app.test_client()
        print(Todo)
        response = client.get('/')
        print(response.get_json)
        assert response.status_code == 200
