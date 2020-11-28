# hw-todo

hw-todo is a todo app for all your assignments which synchronizes with Canvas LMS and let's you add your own assignments.

![alt text](https://github.com/francisseverino/hw-todo/blob/main/screenshots/dashboard.png)

![alt text](https://github.com/francisseverino/hw-todo/blob/main/screenshots/update.png)

### Architecture Diagram

![alt text](https://github.com/francisseverino/hw-todo/blob/main/diagram.png)

## Use cases

 - Log all your assignments instead of using a calendar.
 - Automatically synchronize upcoming assignments from Canvas LMS.
 - Easily keep all your assignments as a simple todo so you don't forget to do your homework again.

## Setup

clone project and create virtual environment

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

### Set environment variables in terminal

Unix Bash (Linux, Mac, etc.):

```bash
$ export FLASK_APP=hw_todo
$ export FLASK_ENV=development
```

or on Windows CMD:

```console
$ set FLASK_APP=hw_todo
$ set FLASK_ENV=development
```

or on Windows PowerShell:

```console
$ $env:FLASK_APP = "hw_todo"
$ $env:FLASK_ENV = "development"
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
