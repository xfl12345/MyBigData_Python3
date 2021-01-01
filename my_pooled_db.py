from dbutils.pooled_db import PooledDB
import db_config as config

"""
@功能：创建数据库连接池
"""


connection_pool = PooledDB(
    creator=config.DB_CREATOR,
    mincached=config.DB_MIN_CACHED,
    maxcached=config.DB_MAX_CACHED,
    maxshared=config.DB_MAX_SHARED,
    maxconnections=config.DB_MAX_CONNECYIONS,
    blocking=config.DB_BLOCKING,
    maxusage=config.DB_MAX_USAGE,
    setsession=config.DB_SET_SESSION,
    host=config.DB_HOST,
    port=config.DB_PORT,
    user=config.DB_USER,
    passwd=config.DB_PASSWORD,
    database=config.DB_DBNAME,
    use_unicode=False,
    charset=config.DB_CHARSET
)

# 从连接池中取出一个共享连接
def get_shared_connection():
    return connection_pool.connection(shareable=True)

# 从连接池中取出一个专用连接
def get_dedicated_connection():
    return connection_pool.connection(shareable=False)

def release_dedicated_connection(conn):
    conn.close()

def release_shared_connection(conn):
    conn.close()

def close_all_connection():
    connection_pool.close()