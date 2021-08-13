from mybigdata.src.main.appconst import data_type_lenght
from mybigdata.src.main.global_variable import json_schema_map

from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main.model.conf import config_manager

from mybigdata.src.main.model.db import my_pooled_db
from mybigdata.src.main.model.db.escape_string import escape_string_for_insert
from mybigdata.src.main.model.db.just_execute_sql import one_row_query

from mybigdata.src.main.model.utils.uuid_generator import UUID_GENERATOR

import jschon
from loguru import logger


# 向 全局ID记录表 插入一行新记录，表明其它表要新增一行数据啦！
def by_table_name(table_name: str) -> int:
    # Generate UUID
    curr_uuid = UUID_GENERATOR.uuid1()
    # 转义字符串，防止SQL注入
    table_name = escape_string_for_insert(table_name)
    # 获取APP核心表名
    global_data_record_table_name = APP_CONFIG.CORE_TABLE_NAME.global_record
    string_type_record_table_name = APP_CONFIG.CORE_TABLE_NAME.string_type
    # 插入一条全局记录
    sql_string = f"insert into {global_data_record_table_name} " \
                 "(uuid, table_name) " \
                 f"values ( '{curr_uuid}', " \
                 f" (select global_id from {string_type_record_table_name} " \
                 f"where content = binary '{table_name}' ));"

    flag, res, exception = one_row_query(sql_string)

    # 如果成功插入一条全局记录，那就获取这个自增的全局ID
    # 如果执行 新增全局ID 的SQL语句失败，意味着没有插入成功
    if flag:
        sql_string = f"select global_id from {global_data_record_table_name} " \
                     f"where uuid = binary '{curr_uuid}';"
        flag, res, exception = one_row_query(sql_string)
        if res is not None and len(res) > 0:
            res = int(res[0])
    return res


def select_global_record_by_global_id(global_id):
    try:
        global_id = int(global_id)
    except Exception as e:
        logger.debug(e)
        return None
    global_data_record_table_name = APP_CONFIG.CORE_TABLE_NAME.global_record
    sql_string = f"select * from {global_data_record_table_name} " \
                 f"where global_id = {global_id};"

    flag, res, exception = one_row_query(sql_string)
    return res


def delete_global_record_by_global_id(global_id) -> bool:
    try:
        global_id = int(global_id)
    except Exception as e:
        logger.debug(e)
        return False
    global_data_record_table_name = APP_CONFIG.CORE_TABLE_NAME.global_record
    sql_string = f"delete from {global_data_record_table_name} " \
                 f"where global_id = {global_id};"

    flag, res, exception = one_row_query(sql_string)
    return flag
