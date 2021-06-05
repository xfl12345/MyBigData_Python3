from flask import Flask, abort, request, jsonify

app = Flask("MyBigData")

# 测试数据暂时存放
tasks = []

# source code URL=https://www.jianshu.com/p/6ac1cab17929
@app.route('/add_task/', methods=['POST'])
def add_task():
    if not request.json or 'id' not in request.json or 'info' not in request.json:
        abort(400)
    task = {
        'id': request.json['id'],
        'info': request.json['info']
    }
    tasks.append(task)
    return jsonify({'result': 'success'})


@app.route('/get_task/', methods=['GET'])
def get_task():
    if not request.args or 'id' not in request.args:
        # 没有指定id则返回全部
        return jsonify(tasks)
    else:
        task_id = request.args['id']
        task = filter(lambda t: t['id'] == int(task_id), tasks)
        return jsonify(task) if task else jsonify({'result': 'not found'})


@app.route("/helloworld")
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
