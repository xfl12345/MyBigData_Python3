import json

import jschon


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, jschon.JSON):
            return obj.value
        return obj.__dict__