from flask import Flask, jsonify, make_response, abort, request
app = Flask(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/api/v1/tasks', methods=['POST'])
def add_task():
    params = validate_json(request, ['title'])

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': params['title'],
        'description': params.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


def validate_json(req, required_params):
    if not req.json:
        abort(400)
    for param in required_params:
        if param not in req.json:
            abort(400)
    return req.json

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "not found"}), 404)

@app.route('/')
def hello_world():
    return 'Free Puntos!'

if __name__ == '__main__':
    app.run(debug=True)
