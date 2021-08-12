from mybigdata.src.main.appconst import data_type_lenght
from mybigdata.src.main.global_veriable import json_schema_map

from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main.model.conf.config_manager import CONFIGURATION_MANAGER

from mybigdata.src.main.model.db import my_pooled_db
from mybigdata.src.main.model.db.escape_string import escape_string_for_insert
from mybigdata.src.main.model.db import process_string_type
from mybigdata.src.main.model.db.just_execute_sql import execute_sql

from mybigdata.src.main.model.utils.uuid_generator import UUID_GENERATOR

import jschon
from loguru import logger


def update_description_using_global_id(global_id, description_global_id):
    try:
        global_id = int(global_id)
        description_global_id = int(description_global_id)
    except Exception as e:
        logger.debug(e)
        return False

    global_data_record_table_name = APP_CONFIG.CORE_TABLE_NAME.global_record
    sql_string = f"UPDATE {global_data_record_table_name} " \
                 f"SET description = {description_global_id} " \
                 f"WHERE global_id = {global_id};"

    flag, res, exception = execute_sql(sql_string)

    return flag


def update_description_using_content(global_id, description: str):
    try:
        global_id = int(global_id)
    except Exception as e:
        logger.error(e)
        return False
    description_global_id = process_string_type.insert_string(description)
    if description_global_id is None:
        return False
    return update_description_using_global_id(global_id, description_global_id)


def select_global_record_by_uuid(uuid):
    try:
        uuid = str(uuid)
    except Exception as e:
        return None
    # 转义字符串，防止SQL注入
    uuid = escape_string_for_insert(uuid)
    global_data_record_table_name = APP_CONFIG.CORE_TABLE_NAME.global_record
    sql_string = f"select * from {global_data_record_table_name} " \
                 f"where uuid = {uuid};"

    flag, res, exception = execute_sql(sql_string)
    return res
