import os
import json

from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main import global_variable
from mybigdata.src.main.model.conf.loader import json_schema_loader
from mybigdata.src.main.model.utils import json_utils

import jschon
from loguru import logger


def reload_resources_directory_path():
    path = os.path.abspath(os.path.dirname(__file__)).split(APP_CONFIG.APP_NAME)[0]
    path = os.path.join(path, "mybigdata/src/main/resources/")
    if os.path.exists(path):
        APP_CONFIG.RESOURCES_DIRECTORY_PATH = path
        APP_CONFIG.update_json_resources_path()


def reload_mybigdata_conf_json_schema():
    flag = False
    full_path = APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH + APP_CONFIG.MYBIGDATA_CONF_FILENAME
    if os.path.exists(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                json_object = jschon.JSONSchema.loads(f.read())
                flag = json_schema_loader.check_and_add_json_schema_to_global_variable(json_object)
        except Exception as e:
            logger.error(e)
    return flag


def reload_mybigdata_conf():
    full_path = APP_CONFIG.JSON_CONFIGURATION_DIRECTORY_PATH + APP_CONFIG.MYBIGDATA_CONF_FILENAME
    if os.path.exists(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                json_conf = json.loads(f.read())
                # 获取文件名（去掉后缀）
                filename_without_suffix = APP_CONFIG.MYBIGDATA_CONF_FILENAME.split(".")[0]
                # Get JSON Schema to validate configuration
                json_schema: jschon.JSONSchema = global_variable.json_schema_map[filename_without_suffix]
                # If the configuration is correct.
                if json_schema.evaluate(jschon.JSON(json_conf)).valid:
                    # Load JSON data directly into a python object.
                    json_utils.dict2class(APP_CONFIG.CORE_TABLE_NAME, json_conf["core"]["table_name"])
        except Exception as e:
            logger.error(e)


def reload_all_json_schema():
    # Load JSON Schema
    json_schema_loader.load_all_schema_from_dir(file_dir_path=APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH)
    json_schema_loader.load_all_schema_from_database()


def reload_all():
    # Load resources path
    reload_resources_directory_path()
    # Load configuration from JSON files
    if reload_mybigdata_conf_json_schema():
        reload_mybigdata_conf()
    # Load JSON schema
    reload_all_json_schema()


reload_all()
