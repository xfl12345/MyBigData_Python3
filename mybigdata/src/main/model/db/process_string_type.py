from mybigdata.src.main.appconst import data_type_lenght
from mybigdata.src.main.global_variable import json_schema_map

from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main.model.conf import config_manager

from mybigdata.src.main.model.db import my_pooled_db
from mybigdata.src.main.model.db.escape_string import escape_string_for_insert
from mybigdata.src.main.model.db import process_global_id
from mybigdata.src.main.model.db.just_execute_sql import one_row_query

from mybigdata.src.main.model.utils.uuid_generator import UUID_GENERATOR

import jschon
from loguru import logger


def insert_string_and_format(string_content: str, data_format: str = "text"):
    pass


# TODO 未完工！！！
# 向数据库插入字符串，成功则返回 数字类型的 global_id ，失败则返回 None
def insert_string(content: str):
    # 因为 插入任意一行数据都要有 全局ID，所以要第一件事就是占用全局ID
    global_id = process_global_id.insert_by_table_name(APP_CONFIG.CORE_TABLE_NAME.string_type)
    if global_id is None:
        return None

    string_content_len = len(content)
    content = escape_string_for_insert(content)
    global_data_record_table_name = APP_CONFIG.CORE_TABLE_NAME.global_record
    string_type_record_table_name = APP_CONFIG.CORE_TABLE_NAME.string_type
    sql_string = f"insert into {string_type_record_table_name} " \
                 f"(global_id, content_length, content) " \
                 f"values ({global_id}, {string_content_len}, '{content}');"

    flag, res, exception = one_row_query(sql_string)

    if flag:
        return global_id
    process_global_id.delete_global_record_by_global_id(global_id)
    return None
