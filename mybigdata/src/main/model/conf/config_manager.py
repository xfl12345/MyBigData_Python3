import json
import jschon
import os

from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main import global_veriable
from mybigdata.src.main.model.conf.loader.json_schema_loader import JsonSchemaLoader
from mybigdata.src.main.model.utils import json_utils


class ConfigurationManager:

    def __init__(self):
        self.json_schema_manager = JsonSchemaLoader()
        self.reload_all()

    def reload_all(self):
        # Load resources path
        self.reload_resources_directory_path()
        # Load JSON schema
        self.reload_all_json_schema()
        # Load configuration from JSON files
        self.reload_mybigdata_conf()

    def reload_resources_directory_path(self):
        path = os.path.abspath(os.path.dirname(__file__)).split(APP_CONFIG.APP_NAME)[0]
        path = os.path.join(path, "mybigdata/src/main/resources/")
        if os.path.exists(path):
            APP_CONFIG.RESOURCES_DIRECTORY_PATH = path
            APP_CONFIG.update_json_resources_path()

    def reload_mybigdata_conf(self):
        full_path = APP_CONFIG.JSON_CONFIGURATION_DIRECTORY_PATH + APP_CONFIG.MYBIGDATA_CONF_FILENAME
        if os.path.exists(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    json_conf = json.loads(f.read())
                    filename_without_suffix = APP_CONFIG.MYBIGDATA_CONF_FILENAME.split(".")[0]
                    # Get JSON Schema to validate configuration
                    json_schema: jschon.JSONSchema = global_veriable.json_schema_map[filename_without_suffix]
                    # If the configuration is correct.
                    if json_schema.evaluate(jschon.JSON(json_conf)).valid:
                        # Load JSON data directly into a python object.
                        json_utils.dict2class(APP_CONFIG.CORE_TABLE_NAME, json_conf["core"]["table_name"])
            except Exception as e:
                print("Failed to reload mybigdata configuration!Error=", e)

    def reload_all_json_schema(self):
        # Load JSON Schema
        self.json_schema_manager.load_all_schema_from_dir(file_dir_path=APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH)
        self.json_schema_manager.load_all_schema_from_database()


CONFIGURATION_MANAGER = ConfigurationManager()
