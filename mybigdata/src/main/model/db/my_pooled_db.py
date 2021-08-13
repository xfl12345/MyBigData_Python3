from dbutils.pooled_db import PooledDB
from mybigdata.src.main.model.conf.app_config import DB_CONFIG

"""
@功能：创建数据库连接池
"""


connection_pool = PooledDB(
    creator=DB_CONFIG.CREATOR,
    mincached=DB_CONFIG.MIN_CACHED,
    maxcached=DB_CONFIG.MAX_CACHED,
    maxshared=DB_CONFIG.MAX_SHARED,
    maxconnections=DB_CONFIG.MAX_CONNECYIONS,
    blocking=DB_CONFIG.BLOCKING,
    maxusage=DB_CONFIG.MAX_USAGE,
    setsession=DB_CONFIG.SET_SESSION,
    host=DB_CONFIG.REMOTE_HOST,
    port=DB_CONFIG.REMOTE_PORT,
    user=DB_CONFIG.AUTH_USER,
    passwd=DB_CONFIG.AUTH_PASSWORD,
    database=DB_CONFIG.DATABASE_NAME,
    use_unicode=DB_CONFIG.USE_UNICODE,
    charset=DB_CONFIG.CHARSET
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