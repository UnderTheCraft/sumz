from flask import Flask

print("This is the wsgi.py file")


def create_app(testing: bool = True):
    print("This is the create_app method")
    app = Flask(__name__)

    @app.route("/")
    def index():
        return f"Hello World!<br>Testing: {testing}"

    return app


application = create_app(testing = True)

print("The application object is now created!")
