import os
import sys

import flask
import flask_restful

from mybigdata.src.main.db_monitor import Monitor

#     monitor_class = monitor()
#     monitor_thread = threading.Thread(target=monitor_class.run,)
#     monitor_thread.start()


if __name__ == "__main__":
    # source code URL=https://www.jianshu.com/p/6ac1cab17929
    app = flask.Flask("MyBigData")
    app.json_encoder.ensure_ascii = False
    app.config["JSON_AS_ASCII"] = False
    # app.json_encoder = NonASCIIJSONEncoder
    app.config["JSONIFY_MIMETYPE"] = "application/json;charset=UTF-8"
    api = flask_restful.Api(app)

    api.add_resource(Monitor, "/monitor")

    app.run(debug=True)
