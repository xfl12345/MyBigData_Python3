from mybigdata.src.main.model.conf.app_config import APP_CONFIG
from mybigdata.src.main.model.conf import config_manager

from mybigdata.src.main.model.db import my_pooled_db
from mybigdata.src.main.model.db.escape_string import escape_string_for_insert

from loguru import logger


def one_row_query(sql_string: str):
    res = None
    flag = False
    exception = None

    conn = None
    try:
        logger.debug(sql_string)
        conn = my_pooled_db.get_shared_connection()

        conn.begin()
        cursor = conn.cursor()
        cursor.execute(sql_string)
        conn.commit()

        res = cursor.fetchone()
        logger.debug(sql_string + " -> " + str(res))
        flag = True
    except Exception as e:
        exception = e
        if conn is not None:
            conn.rollback()
        logger.error(e)

    if conn is not None:
        my_pooled_db.release_shared_connection(conn)

    return flag, res, exception

