# hw-todo

hw-todo is a todo app for all your assignments which synchronizes with Canvas LMS and let's you add your own assignments.

## Setup

Create project with virtual environment

```bash
$ cd hw-todo
$ python3 -m venv venv
```

Activate it
```bash
$ . venv/bin/activate
```

or on Windows
```console
$ venv\Scripts\activate
```

### Install Dependencies

From requirements.txt
```bash
$ pip install -r requirements.txt
```

or Install each dependency
```bash
$ pip install Flask
$ pip install Flask-SQLAlchemy
$ pip install python-dotenv
$ pip install requests
```

Set envoronment variables in terminal

```bash
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
```

or on Windows
```console
$ set FLASK_APP=app.py
$ set FLASK_ENV=development
```

## Usage

Run the app
```bash
$ flask run
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
Jack Fineanganofo & Francis Severino
