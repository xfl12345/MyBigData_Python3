import db_dbutils_init

myTestConnectionPool = db_dbutils_init.get_my_connection();

sqlStr = "select * from test_table;";
cursor, conn = myTestConnectionPool.getconn();

cursor.execute(sqlStr);
res = cursor.fetchone();
print(res);
res = cursor.fetchone();
print(res);

cursor.close();
conn.close();













