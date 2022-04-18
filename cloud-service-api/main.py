from flask import Flask, redirect
from controllers.incidencias import incidencias

app = Flask(__name__)

app.register_blueprint(incidencias)


@app.route('/', methods=['GET'])
def get_swagger():
    return redirect("http://ptin2022.github.io/A2/", 301)


if __name__ == "__main__":
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
