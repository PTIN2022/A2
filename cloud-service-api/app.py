from utils.db import db
from flask import Flask
from routes.incidencias import incidencias


def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"  # TODO: Pass to mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False

app.register_blueprint(incidencias)

if app.config["TESTING"] is False:
    init_db()

if __name__ == "__main__":
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
