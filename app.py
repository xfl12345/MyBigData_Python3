import os
import sys

import flask
import flask_restful

from mybigdata.src.main.db_monitor import Monitor

if __name__ == "__main__":
    # source code URL=https://www.jianshu.com/p/6ac1cab17929
    # source code URL=https://flask-restful.readthedocs.io/en/latest/quickstart.html
    app = flask.Flask("MyBigData")
    app.json_encoder.ensure_ascii = False
    app.config["JSON_AS_ASCII"] = False
    # app.json_encoder = NonASCIIJSONEncoder
    app.config["JSONIFY_MIMETYPE"] = "application/json;charset=UTF-8"
    api = flask_restful.Api(app)

    # 添加 Monitor 监视器到路由
    api.add_resource(Monitor, "/monitor", "/")



    # 启用Flask框架的调试模式（可以热重新加载Python源码）
    app.run(debug=True)
