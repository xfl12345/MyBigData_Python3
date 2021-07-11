from pymysql.converters import escape_string


def escape_string_for_query(input_string: str):
    # 消灭普通字符串注入攻击
    input_string = escape_string(input_string)
    # 消灭可执行模糊匹配的通配符
    input_string = input_string.replace("@", "\@").replace("_", "\_")
    return input_string

def escape_string_for_insert(input_string: str):
    # 消灭普通字符串注入攻击
    input_string = escape_string(input_string)
    return input_string
