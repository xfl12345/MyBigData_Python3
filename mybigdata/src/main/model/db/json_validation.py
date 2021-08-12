from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main.global_veriable import json_schema_map

import jschon


def valid_json(json_object: jschon.JSON, json_schema_name: str):
    if json_schema_name is None or \
            not (json_schema_name in json_schema_map.keys()):
        return False
    json_schema: jschon.JSONSchema = json_schema_map[json_schema_name]
    return json_schema.evaluate(json_object).valid


def valid_json_string(content: str, json_schema_name: str):
    json_object = jschon.JSON.loads(content)
    return valid_json(json_object, json_schema_name)
