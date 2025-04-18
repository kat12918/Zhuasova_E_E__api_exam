from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
api = Api(app)

# Временное хранилище задач
tasks = {}
task_id_counter = 1

# Схема для валидации задачи
class TaskSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    status = fields.Str(required=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class TaskResource(Resource):
    def get(self):
        """Получить список всех задач"""
        return tasks_schema.dump(tasks.values()), 200

    def post(self):
        """Создать новую задачу"""
        global task_id_counter
        try:
            task_data = task_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        task_data['id'] = task_id_counter
        tasks[task_id_counter] = task_data
        task_id_counter += 1
        return task_data, 201

class TaskDetailResource(Resource):
    def put(self, task_id):
        """Обновить задачу по ID"""
        if task_id not in tasks:
            return {"message": "Task not found"}, 404

        try:
            task_data = task_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        task_data['id'] = task_id
        tasks[task_id] = task_data
        return task_data, 200

    def delete(self, task_id):
        """Удалить задачу по ID"""
        if task_id not in tasks:
            return {"message": "Task not found"}, 404

        del tasks[task_id]
        return {"message": "Task deleted"}, 200

# Регистрация маршрутов
api.add_resource(TaskResource, '/tasks')
api.add_resource(TaskDetailResource, '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)