from mybigdata.src.main.model.db import my_pooled_db
from mybigdata.src.main import global_veriable

import flask
import flask_restful

# TODO 改造RESTful API 使得访问URL即访问 dict 路径，
#  访问URL即按 类名 定位资源，
#  例如：
#  访问 http:// address : port / Monitor ，即访问 Monitor 的根，
#  访问 http:// address : port / Monitor / the_pool ，即访问 Monitor.the_pool 的根，
#  以此类推……

class Monitor(flask_restful.Resource):
    the_pool = None

    def __init__(self):
        self.the_pool = my_pooled_db.connection_pool

    def get(self):
        response_data = {}
        if hasattr(self.the_pool, "_connections"):
            response_data["connections_count"] = self.the_pool._connections
        if hasattr(self.the_pool, "_shared_cache"):
            response_data["shared_cache_count"] = len(self.the_pool._shared_cache)
        if hasattr(self.the_pool, "_idle_cache"):
            response_data["idle_cache_count"] = len(self.the_pool._idle_cache)

        json_schema_map_dict = {}
        for name, json_schema in global_veriable.json_schema_map.items():
            json_schema_map_dict[name] = json_schema.value
        # print(json_schema_map_dict)
        response_data = {
            "database_connection_pool": response_data,
            "global_veriable": {
                "json_schema_map": json_schema_map_dict
            }
        }

        return flask.make_response(response_data)
