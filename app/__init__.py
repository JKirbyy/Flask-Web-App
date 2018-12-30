from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api

app = Flask(__name__)
app.config.from_object('config')

# Check Configuration section for more details

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#api = Api(app)

tasks = {}


class TaskResource(Resource):
    def get(self, task_id):
        return {task_id: tasks[task_id]}

    def put(self, task_id):
        tasks[task_id] = request.form['data']
        return {task_id: tasks[task_id]}


#pi.add_resource(TaskResource, '/<string:task_id>')

from app import forms, home, models, post, profile, run, search, login, create
