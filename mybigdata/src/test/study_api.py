import json

from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource

# class NonASCIIJSONEncoder(json.JSONEncoder):
#     def __init__(self, **kwargs):
#         kwargs['ensure_ascii'] = False
#         super(NonASCIIJSONEncoder, self).__init__(**kwargs)

# source code URL=https://www.jianshu.com/p/6ac1cab17929
app = Flask("MyBigData")
app.json_encoder.ensure_ascii = False
app.config["JSON_AS_ASCII"] = False
# app.json_encoder = NonASCIIJSONEncoder
app.config["JSONIFY_MIMETYPE"] = "application/json;charset=UTF-8"
api = Api(app)

TODOS = {
    "todo1": {"task": "build an API"},
    "todo2": {"task": "哈哈哈"},
    "todo3": {"task": "profit!"},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} does not exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument("task")


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return make_response(TODOS[todo_id])
        # return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return make_response("", 204)

    def put(self, todo_id):
        args = parser.parse_args()
        task = {"task": args["task"]}
        TODOS[todo_id] = task
        return make_response(task, 201)


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        res = make_response(TODOS, 200)
        return res

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip("todo")) + 1
        todo_id = "todo%i" % todo_id
        TODOS[todo_id] = {"task": args["task"]}
        return make_response(TODOS[todo_id], 201)


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, "/todos")
api.add_resource(Todo, "/todos/<todo_id>")

if __name__ == "__main__":
    app.run(debug=True)