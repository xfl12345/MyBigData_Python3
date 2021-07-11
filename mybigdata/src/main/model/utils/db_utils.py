from mybigdata.src.main.model.db import my_pooled_db


def one_row_query(sql_string: str):
    res = None
    try:
        conn = my_pooled_db.get_shared_connection()
        cursor = conn.cursor()
        cursor.execute(sql_string)
        res = cursor.fetchone()
        cursor.close()
        my_pooled_db.release_shared_connection(conn)
    except Exception:
        pass
    return res

