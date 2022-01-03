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
                    json_utils.dict2object(APP_CONFIG.CORE_TABLE_NAME, json_conf["core"]["table_name"])
        except Exception as e:
            logger.error(e)


def reload_all_json_schema():
    # Load JSON Schema
    json_schema_loader.load_all_schema_from_dir(file_dir_path=APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH)
    json_schema_loader.load_all_schema_from_database()


"""
加载配置的逻辑：
1.重新加载本地资源文件路径（注意，是 路径）。
  将更新 APP_CONFIG 里的 JSON_RESOURCES_DIRECTORY_PATH 、 
  JSON_SCHEMA_DIRECTORY_PATH 和 JSON_CONFIGURATION_DIRECTORY_PATH
  这几个家伙的值。他们都是路径。
2.从 APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH 尝试加载 
  APP_CONFIG.MYBIGDATA_CONF_FILENAME 所记录的 JSON模型文件 到 全局变量 json_schema_map。
  为进一步验证 APP 的 JSON配置文件 是否符合要求提供检验标准
3.如果 APP_CONFIG.MYBIGDATA_CONF_FILENAME 所记录的 JSON模型文件 符合自身所记录的规范，
  则尝试从本地加载 APP 的 JSON配置文件 ，并配置 APP 应用程序。
4.重新加载所有 JSON模型文件 。优先从本地加载，然后从数据库里加载。
  数据库里如果存在同名 JSON模型 ，将会覆盖为数据库版本。
"""


def reload_all():
    # Load resources path
    reload_resources_directory_path()
    # Load configuration from JSON files
    if reload_mybigdata_conf_json_schema():
        reload_mybigdata_conf()
    # Load JSON schema
    reload_all_json_schema()
