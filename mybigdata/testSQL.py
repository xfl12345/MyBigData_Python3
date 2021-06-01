import my_pooled_db

sqlStr = "select * from test_table;"


conn = my_pooled_db.get_shared_connection()

cursor = conn.cursor()
cursor.execute(sqlStr)
res = cursor.fetchone()
print(res)
res = cursor.fetchone()
print(res)

cursor.close()
my_pooled_db.release_shared_connection(conn)













