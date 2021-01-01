首先要解决这个“数据库连接池”问题
嗯……怎么搞啊？？？

一番谷歌搜索“Python3 连接MySQL 连接池”
约束搜索引擎，只显示过去1年以内的结果
找到这篇博客：<https://www.cnblogs.com/jiangxiaobo/p/12786205.html>
其中提到：

>需要库
>1、DBUtils pip install DBUtils
>2、pymysql pip install pymysql/MySQLdb

所以……pymysql和MySQLdb有什么不一样？选哪个好？
百度搜索“pymysql和MySQLdb”
结果找到这个：<https://www.cnblogs.com/yuhou/p/10868831.html>
所以还是使用pymysql貌似比较稳，而且我们要找的“连接池”，这个家伙有，
而MySQLdb貌似没有。。
所以果断使用pymysql啦！
马上，管理员身份运行CMD执行命令：`pip3 install pymysql`

然后按照博客给的范文，完整地把代码复制下来。。
发现Visual Studio Code说这个"db_dbutils_init.py"的第1行
`from DBUtils.PooledDB import PooledDB`有错误，
说是这个"PooledDB"找不到，我按住Ctrl键然后鼠标左键点击这个"DBUtils"，
发现可以点进去，说明DBUtils还是安装成功了的，有这个包，
看了看 DBUtils 的 "__init__.py"文件内容：

```python
# DBUtils main package

__all__ = [
    '__version__',
    'simple_pooled_pg', 'steady_pg', 'pooled_pg', 'persistent_pg',
    'simple_pooled_db', 'steady_db', 'pooled_db', 'persistent_db']

__version__ = '2.0'
```

咦？"pooled_db"？？？
随即改了一下代码：
`from DBUtils.pooled_db import PooledDB`
然后Visual Studio Code就不提示这行有错了（然而这里有坑）
为了确定为什么我的代码和别人的代码有出入，以及弄明白db_config里的东西和PooledDB到底怎么用，
随即又去谷歌一番，查找官方开发文档，搜索“python3 DBUtils.pooled_db”
结果找到这个：<https://webwareforpython.github.io/DBUtils/main.html#pooleddb-pooled-db>

看看，感觉很难的样子，然后我又看了一下这篇博客的"mysqLhelper.py"是怎么实现的
感觉还是很复杂，功能好像很高级，但很有可能过时了，因为版本有变化
所以为了习得技术，得自己另外写一个程序测试一下
搞个"testSQL.py"，内容如下：

```python
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
```

修改"db_config.py"里的配置信息，去phpmyadmin在数据库里添加一个权限有范围的普通账号
数据库里添加一个表“test_table”，顺便添加点东西以供测试

```sql
START TRANSACTION;
DROP TABLE IF EXISTS `test_table`;
CREATE TABLE IF NOT EXISTS `test_table` (
  `ID` int(11) NOT NULL,
  `num` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
INSERT INTO `test_table` (`ID`, `num`) VALUES
(1, 666),
(233, 678);
COMMIT;
```


为了防止出现意外，我又去确定配置有没有问题（毕竟跨版本），
又去查阅了 DBUtils.pooled_db 的源码，
发现连接数据库的标准写法好像有点出入，
在"pooled_db.py"的 第 78 行：
`pool = PooledDB(pgdb, 5, database='mydb')`
随即修改了一下"db_dbutils_init.py"的 第 37 行，
把 "db" 改成了 "database"

激动人心的时刻来了，马上运行一下，看看能不能跑通。
结果报错：`ModuleNotFoundError: No module named 'DBUtils'`
巴拉巴拉的。。

立刻百度搜索这个错误信息，
结果找到这个：<https://www.pythonf.cn/read/158325>

于是得知，DBUtils的v1.3版本是这样写的：
from DBUtils.PooledDB import PooledDB
DBUtils的v2.0版本却要这样写的：
from dbutils.pooled_db import PooledDB

顿时就傻了，我不是改过来了吗？
我反复对比，定眼一看，啊！
`from Dbutils.pooled_db import PooledDB`
里的"Dbutils"里的"D"不是大写！
马上改成小写的"d"：
`from dbutils.pooled_db import PooledDB`
修复BUG，然后为了以防万一，我还直接复制粘贴他的这行代码
确保万无一失。。。

代码跑通了。。

```powershell
PS E:\Data\project\2020_MyBigData\MyBigData_Python3>  & 'C:\Program Files\Python38\python.exe' 'E:\sysdata\xfl666\.vscode\extensions\ms-python.python-2020.12.424452561\pythonFiles\lib\python\debugpy\launcher' '45318' '--' 'e:\Data\project\2020_MyBigData\MyBigData_Python3\testSQL.py'
(1, 666)
(233, 678)
```

重新整理了一下学习log，因为之前学习的时候并没有做跟踪记录
后来重新再走一遍学习过程写出来的，文章顺序不自然
（因为躺了坑之后，把坑填平了，然后又忘记是怎么被坑的，XD）

我发现这篇博客<https://www.cnblogs.com/jiangxiaobo/p/12786205.html>
开始写得还好，具有引导性，到后面我仔细想了想
我们需要的是 **单例模式** 的连接池，不然多线程会有海量开销
然而………作者把它写成了一个类，这就挺迷的……
如果以模块的形式导入到其它Python文件，据说可以保证是单例
但是写成一个类难道不是多此一举？

于是我索性简化了一番……



