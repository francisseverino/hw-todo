from hw_todo import app

@app.route('/')
def index():
    return 'Hello World!'