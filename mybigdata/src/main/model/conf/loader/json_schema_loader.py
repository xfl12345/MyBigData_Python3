import os
import json
import jschon

from loguru import logger

from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main import global_variable
from mybigdata.src.main.model.db import my_pooled_db
from mybigdata.src.main.model.db.escape_string import escape_string_for_insert
from mybigdata.src.main.model.db.just_execute_sql import one_row_query


def get_root_path() -> str:
    return os.path.abspath(os.path.dirname(__file__)).split(APP_CONFIG.APP_NAME)[0]


def get_json_schema_resources_root_path() -> str:
    if os.path.exists(APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH):
        return APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH
    relative_path = APP_CONFIG.JSON_SCHEMA_DIRECTORY_PATH
    absolute_path = get_root_path()
    full_path = os.path.join(absolute_path, relative_path)
    if os.path.exists(full_path):
        absolute_path = full_path
        absolute_path = os.path.abspath(absolute_path)
        return absolute_path
    else:
        return relative_path


def get_schema_from_file(file_name: str, file_dir_path: str = None):
    if file_dir_path is None:
        file_dir_path = get_root_path()
    json_schema = None
    # 优先看看本地目录下有无现成json文件
    json_file_path = os.path.join(file_dir_path, file_name, ".json")
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_schema_python_object = json.loads(f.read())
            # 验证是否 是合法的 JSON Schema
            try:
                json_schema = jschon.JSONSchema(json_schema_python_object).validate()
            except Exception as e:
                logger.error(e)
    return json_schema


def get_schema_from_database(schema_name: str):
    json_schema = None
    # 查询字符串防注入（特殊符号转义）
    schema_name = escape_string_for_insert(schema_name)
    # 获取APP核心表名
    global_data_record_table_name = APP_CONFIG.CORE_TABLE_NAME.global_record
    string_type_record_table_name = APP_CONFIG.CORE_TABLE_NAME.string_type.content
    # 构建SQL查询语句
    sql_string = f"select json_schema from {global_data_record_table_name}," \
                 f"{string_type_record_table_name} as s " \
                 f"where schema_name = s.global_id and s.content = '{schema_name}';"
    # 只有一行结果的查询
    flag, res, exception = one_row_query(sql_string)
    if res is not None:
        # JSON Schema 在第1列
        json_schema_python_object = json.loads(res[0])
        # 验证是否 是合法的 JSON Schema
        try:
            json_schema = jschon.JSONSchema(json_schema_python_object)
            if not json_schema.validate().valid:
                json_schema = None
        except Exception as e:
            logger.error(e)
    return json_schema


def check_and_add_json_schema_to_global_variable(json_schema_python_object: jschon.JSONSchema):
    is_succeed = False
    # 验证是否 是合法的 JSON Schema
    try:
        # 如果合法，加入到内存，高速缓存
        if json_schema_python_object.validate().valid:
            schema_name = json_schema_python_object.value["title"]
            global_variable.json_schema_map[schema_name] = json_schema_python_object
            is_succeed = True
    except Exception as e:
        logger.error(e)
    return is_succeed


def load_all_schema_from_dir(file_dir_path: str = None):
    if file_dir_path is None:
        file_dir_path = get_root_path()
    # 权威性： 本地文件 < 数据库 （若后者数据若与前者同名，则后者数据将覆盖前者）
    # 从本地文件加载 JSON Schema
    for root, dirs, files in os.walk(file_dir_path, topdown=False):
        for name in files:
            json_file_path = os.path.join(root, name)
            logger.info("Loading json schema file=" + json_file_path)
            with open(json_file_path, "r", encoding="utf-8") as f:
                json_schema_python_object = jschon.JSONSchema.loads(f.read())
                check_and_add_json_schema_to_global_variable(json_schema_python_object)


def load_all_schema_from_database():
    # 从数据库加载 JSON Schema
    # 获取APP核心表名
    table_schema_record_table_name = APP_CONFIG.CORE_TABLE_NAME.table_schema_record.record
    # 构建SQL查询语句
    sql_string = f"select json_schema from {table_schema_record_table_name};"
    conn = None
    try:
        conn = my_pooled_db.get_shared_connection()

        cursor = conn.cursor()
        cursor.execute(sql_string)

        keep_loop_flag = True
        i = 0
        while keep_loop_flag:
            res = cursor.fetchone()
            if res is not None:
                logger.debug(sql_string + f" [{i}]-> " + str(res))
                # JSON Schema 在第1列
                json_schema_python_object = jschon.JSONSchema.loads(res[0])
                check_and_add_json_schema_to_global_variable(json_schema_python_object)
                i = i + 1
            else:
                keep_loop_flag = False

        cursor.close()
        my_pooled_db.release_shared_connection(conn)
    except Exception as e:
        if conn is not None:
            conn.rollback()
        logger.error(e)
    if conn is not None:
        my_pooled_db.release_shared_connection(conn)

