from . import data_type

# mysql 5.7的数据类型长度范围，长度单位： Byte
mysql5p7 = {
    # 固定长度的数据类型
    "fixed": {
        data_type.Mysql5p7.TINYINT: 1,
        data_type.Mysql5p7.SMALLINT: 2,
        data_type.Mysql5p7.MEDIUMINT: 3,
        data_type.Mysql5p7.INTEGER: 4,
        # data_type.Mysql5p7.INT: 4,
        data_type.Mysql5p7.BIGINT: 8,

        data_type.Mysql5p7.FLOAT: 4,
        data_type.Mysql5p7.DOUBLE: 8,

        data_type.Mysql5p7.DATE: 3,
        data_type.Mysql5p7.TIME: 3,
        data_type.Mysql5p7.YEAR: 1,
        data_type.Mysql5p7.DATETIME: 8,
        data_type.Mysql5p7.TIMESTAMP: 4,
    },
    # 可变长度的数据类型（范围可以用 固定的最小值 和 固定的最大值 来表示的）
    "variable": {
        data_type.Mysql5p7.CHAR: (0, (1 << 8) - 1),
        data_type.Mysql5p7.VARCHAR: (0, (1 << 16) - 1),

        data_type.Mysql5p7.TINYBLOB: (0, (1 << 8) - 1),
        data_type.Mysql5p7.BLOB: (0, (1 << 16) - 1),
        data_type.Mysql5p7.MEDIUMBLOB: (0, (1 << 24) - 1),
        data_type.Mysql5p7.LONGBLOB: (0, (1 << 32) - 1),

        data_type.Mysql5p7.TINYTEXT: (0, (1 << 8) - 1),
        data_type.Mysql5p7.TEXT: (0, (1 << 16) - 1),
        data_type.Mysql5p7.MEDIUMTEXT: (0, (1 << 24) - 1),
        data_type.Mysql5p7.LONGTEXT: (0, (1 << 32) - 1),

    },
    # 特殊的可变长度的数据类型
    "special-variable": {
        data_type.Mysql5p7.DECIMAL: ((1, 65), (0, 30)),
        # data_type.Mysql5p7.DEC: ((1, 65), (0, 30)),
    },

}
