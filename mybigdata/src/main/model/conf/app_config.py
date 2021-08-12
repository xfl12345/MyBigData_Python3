# -*- coding: UTF-8 -*-
import pymysql
import jschon
import os

from mybigdata.src.main.appconst import commons

CATALOGUE = jschon.Catalogue.create_default_catalogue("2020-12")


class DbConfig:
    # 数据库信息
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "xfl"
    DB_PASSWORD = "amazingxfl666"
    DB_DBNAME = "xfl_mybigdata"

    # 数据库连接编码
    DB_CHARSET = "utf8"
    DB_USE_UNICODE = True

    # mincached : 启动时开启的闲置连接数量(缺省值 0 开始时不创建连接)
    DB_MIN_CACHED = 10

    # maxcached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
    DB_MAX_CACHED = 10

    # maxshared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
    DB_MAX_SHARED = 20

    # maxconnecyions : 创建连接池的最大数量(缺省值 0 代表不限制)
    DB_MAX_CONNECYIONS = 100

    # blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误<toMany......> 其他代表阻塞直到连接数减少,连接被分配)
    DB_BLOCKING = True

    # maxusage : 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
    DB_MAX_USAGE = 0

    # setsession : 一个可选的SQL命令列表用于准备每个会话，如["set datestyle to german", ...]
    DB_SET_SESSION = None

    # creator : 使用连接数据库的模块
    DB_CREATOR = pymysql

    def __init__(self):
        pass


# APP内建的 数据库表 的名称
class CoreTableName:
    global_record = "global_data_record"
    string_type = None
    number_type = None
    array_type = None
    boolean_type = None


class AppConfig:
    APP_NAME: str = "mybigdata"

    MYBIGDATA_CONF_FILENAME: str = "mybigdata_configuration.json"

    # 资源文件夹默认的相对路径常量
    RESOURCES_DIRECTORY_PATH: str = "mybigdata/src/main/resources/"

    def __init__(self):
        self.JSON_RESOURCES_DIRECTORY_PATH: str = os.path.join(self.RESOURCES_DIRECTORY_PATH, "json/")
        self.JSON_SCHEMA_DIRECTORY_PATH: str = os.path.join(self.JSON_RESOURCES_DIRECTORY_PATH, "schema/")
        self.JSON_CONFIGURATION_DIRECTORY_PATH: str = os.path.join(self.JSON_RESOURCES_DIRECTORY_PATH, "conf/")
        # APP内建的 数据库表 的名称
        self.CORE_TABLE_NAME = CoreTableName()

    def update_json_resources_path(self):
        self.JSON_RESOURCES_DIRECTORY_PATH: str = os.path.join(self.RESOURCES_DIRECTORY_PATH, "json/")
        self.JSON_SCHEMA_DIRECTORY_PATH: str = os.path.join(self.JSON_RESOURCES_DIRECTORY_PATH, "schema/")
        self.JSON_CONFIGURATION_DIRECTORY_PATH: str = os.path.join(self.JSON_RESOURCES_DIRECTORY_PATH, "conf/")


APP_CONFIG = AppConfig()
DB_CONFIG = DbConfig()
