from dbutils.pooled_db import PooledDB
from mybigdata.src.main.model.conf.app_config import DB_CONFIG

"""
@功能：创建数据库连接池
"""


connection_pool = PooledDB(
    creator=DB_CONFIG.DB_CREATOR,
    mincached=DB_CONFIG.DB_MIN_CACHED,
    maxcached=DB_CONFIG.DB_MAX_CACHED,
    maxshared=DB_CONFIG.DB_MAX_SHARED,
    maxconnections=DB_CONFIG.DB_MAX_CONNECYIONS,
    blocking=DB_CONFIG.DB_BLOCKING,
    maxusage=DB_CONFIG.DB_MAX_USAGE,
    setsession=DB_CONFIG.DB_SET_SESSION,
    host=DB_CONFIG.DB_HOST,
    port=DB_CONFIG.DB_PORT,
    user=DB_CONFIG.DB_USER,
    passwd=DB_CONFIG.DB_PASSWORD,
    database=DB_CONFIG.DB_DBNAME,
    use_unicode=DB_CONFIG.DB_USE_UNICODE,
    charset=DB_CONFIG.DB_CHARSET
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