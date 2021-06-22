import json
from mybigdata.src.main.utils.encoder import MyJSONEncoder
from . import data_type


class BaseStruct(object):
    # 整数类型（集合）
    number = None
    # 使用IEEE 754标准的浮点数类型（集合）
    IEEE754 = None
    # 时间类型（集合）
    time = None
    # 字符串类型（集合）
    string = None
    # 特殊类型（集合)
    special = None

    def to_json_string(self):
        return json.dumps(self, cls=MyJSONEncoder, sort_keys=True, indent=4)


# mysql 5.7的数据类型分类
class MySQL5p7(BaseStruct):
    def __init__(self):
        BaseStruct.__init__(self)
        # 整数类型（集合）
        self.number = {
            data_type.Mysql5p7.TINYINT,
            data_type.Mysql5p7.SMALLINT,
            data_type.Mysql5p7.MEDIUMINT,
            # data_type.Mysql5p7.INT,
            data_type.Mysql5p7.INTEGER,
            data_type.Mysql5p7.BIGINT,
        }
        # 使用IEEE 754标准的浮点数类型（集合）
        self.IEEE754 = {
            data_type.Mysql5p7.FLOAT,
            data_type.Mysql5p7.DOUBLE,
        }
        # 时间类型（集合）
        self.time = {
            data_type.Mysql5p7.DATE,
            data_type.Mysql5p7.TIME,
            data_type.Mysql5p7.YEAR,
            data_type.Mysql5p7.DATETIME,
            data_type.Mysql5p7.TIMESTAMP,
        }
        # 字符串类型（集合）
        self.string = {
            data_type.Mysql5p7.CHAR,
            data_type.Mysql5p7.VARCHAR,

            data_type.Mysql5p7.TINYBLOB,
            data_type.Mysql5p7.BLOB,
            data_type.Mysql5p7.MEDIUMBLOB,
            data_type.Mysql5p7.LONGBLOB,

            data_type.Mysql5p7.TINYTEXT,
            data_type.Mysql5p7.TEXT,
            data_type.Mysql5p7.MEDIUMTEXT,
            data_type.Mysql5p7.LONGTEXT,
        }
        # 特殊类型（集合)
        self.special = {
            data_type.Mysql5p7.DECIMAL,
        }


# 单例
mysql5p7 = MySQL5p7()
