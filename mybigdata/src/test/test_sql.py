from mybigdata.src.main.model.db import my_pooled_db
from mybigdata.src.main.appconst import data_type_lenght
from pymysql.converters import escape_string

print(data_type_lenght.mysql5p7)


def executeSqlStr(sql_string):
    print(sql_string)
    conn = my_pooled_db.get_shared_connection()

    cursor = conn.cursor()
    cursor.execute(sql_string)
    res = cursor.fetchone()
    print(res)
    res = cursor.fetchone()
    print(res)

    cursor.close()
    my_pooled_db.release_shared_connection(conn)


sql_string = "select * from test_table;"
executeSqlStr(sql_string)

schema_name = ''' "';666%-- ~!@#$%^&*()_+`1234567890-={}|[]\;\': '''
schema_name = escape_string(schema_name)
schema_name = schema_name.replace("@", "\@")
schema_name = schema_name.replace("_", "\_")
sql_string = "select * from string_content where string_content = '{}';".format(schema_name)
executeSqlStr(sql_string)

schema_name = '\u4e2d\u6587'
schema_name = escape_string(schema_name)
sql_string = "select * from string_content where string_content = '{}';".format(schema_name)
executeSqlStr(sql_string)

schema_name = '新增字符串'
schema_name = escape_string(schema_name)
sql_string = "select * from table_schema_record,string_content as s " \
             "where schema_name = s.global_id and s.string_content = '{}';".format(schema_name)
print(sql_string)
conn = my_pooled_db.get_shared_connection()

cursor = conn.cursor()
cursor.execute(sql_string)
res = cursor.fetchone()
print(res)
print(res[3])

cursor.close()
my_pooled_db.release_shared_connection(conn)

