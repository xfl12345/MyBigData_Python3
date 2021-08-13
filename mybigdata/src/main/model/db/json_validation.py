from mybigdata.src.main.global_variable import json_schema_map

import jschon
from loguru import logger


def valid_json(json_object: jschon.JSON, json_schema_name: str):
    # 优先判断是否为空，若否则检查字典里是否存在传入的 json_schema_name
    if json_object is None or json_schema_name is None or \
            not (json_schema_name in json_schema_map.keys()):
        return False
    json_schema: jschon.JSONSchema = json_schema_map[json_schema_name]
    return json_schema.evaluate(json_object).valid


def valid_json_string(content: str, json_schema_name: str):
    try:
        json_object = jschon.JSON.loads(content)
    except Exception as e:
        logger.error(e)
        return False
    return valid_json(json_object, json_schema_name)
