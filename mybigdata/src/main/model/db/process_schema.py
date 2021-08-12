from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main.global_veriable import json_schema_map

import jschon


class ProcessSchema:
    def __init__(self):
        pass

    def insert(self, content: str):
        json_schema_name: str = APP_CONFIG.CORE_TABLE_NAME.string_type
        if json_schema_name is None or \
                not (json_schema_name in json_schema_map.keys()):
            return False
        json_schema: jschon.JSONSchema = json_schema_map[json_schema_name]
        if json_schema.evaluate( jschon.JSON.loads(content) ).valid:
            pass
