from flask import Flask

print("This is the wsgi.py file")

def create_app(testing: bool = True):
    print("This is the create_app method")
    application = Flask(__name__)

    @application.route("/")
    def index():
        return f"Hello World!<br>Testing: {testing}"

    return application