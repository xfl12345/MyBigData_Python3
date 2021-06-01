# 学习日志

首先要解决这个“数据库连接池”问题  
嗯……怎么搞啊？？？

一番谷歌搜索“Python3 连接MySQL 连接池”  
约束搜索引擎，只显示过去1年以内的结果  
找到这篇博客：<https://www.cnblogs.com/jiangxiaobo/p/12786205.html>
其中提到：  

>需要库  
> 
>1、DBUtils   
> pip install DBUtils  
> 
>2、pymysql  
> pip install pymysql/MySQLdb  

所以……pymysql和MySQLdb有什么不一样？选哪个好？  
百度搜索“pymysql和MySQLdb”  
结果找到这个：<https://www.cnblogs.com/yuhou/p/10868831.html>  
所以还是使用pymysql貌似比较稳，而且我们要找的“连接池”，这个家伙有，  
而MySQLdb貌似没有。。  
所以果断使用pymysql啦！  
马上，管理员身份运行CMD执行命令：`pip3 install pymysql`  

然后按照博客给的范文，完整地把代码复制下来。。  
发现Visual Studio Code说这个 `db_dbutils_init.py` 的第1行  
`from DBUtils.PooledDB import PooledDB`有错误，  
说是这个"PooledDB"找不到，我按住Ctrl键然后鼠标左键点击这个 `DBUtils` ，  
发现可以点进去，说明 `DBUtils` 还是安装成功了的，有这个包，  
看了看 DBUtils 的 `__init__.py` 文件内容：  

```text
# DBUtils main package

__all__ = [
    '__version__',
    'simple_pooled_pg', 'steady_pg', 'pooled_pg', 'persistent_pg',
    'simple_pooled_db', 'steady_db', 'pooled_db', 'persistent_db']

__version__ = '2.0'
```

咦？"pooled_db"？？？  
随即改了一下代码：`from DBUtils.pooled_db import PooledDB`  
然后Visual Studio Code就不提示这行有错了（然而这里有坑）  
为了确定为什么我的代码和别人的代码有出入，  
以及弄明白db_config里的东西和PooledDB到底怎么用，  
随即又去谷歌一番，查找官方开发文档，搜索“python3 DBUtils.pooled_db”  
结果找到这个：<https://webwareforpython.github.io/DBUtils/main.html#pooleddb-pooled-db>  

看看，感觉很难的样子，  
然后我又看了一下这篇博客的 **mysqLhelper.py** 是怎么实现的  
感觉还是很复杂，功能好像很高级，但很有可能过时了，因为版本有变化  
所以为了习得技术，得自己另外写一个程序测试一下  
搞个 **testSQL.py** ，内容如下：  

```text
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

修改 **db_config.py** 里的配置信息，
去phpmyadmin在数据库里添加一个权限有范围的普通账号  
数据库里添加一个表 **test_table** ，顺便添加点东西以供测试  

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
在 **pooled_db.py** 的 第 78 行：  
`pool = PooledDB(pgdb, 5, database='mydb')`  
随即修改了一下 **db_dbutils_init.py** 的 第 37 行，把 "db" 改成了 "database"

激动人心的时刻来了，马上运行一下，看看能不能跑通。  
结果报错：`ModuleNotFoundError: No module named 'DBUtils'`  
巴拉巴拉的。。  

立刻百度搜索这个错误信息，  
结果找到这个：<https://www.pythonf.cn/read/158325>  

于是得知，DBUtils的v1.3版本是这样写的：  
`from DBUtils.PooledDB import PooledDB`  
DBUtils的v2.0版本却要这样写的：  
`from dbutils.pooled_db import PooledDB`  

顿时就傻了，我不是改过来了吗？  
我反复对比，定眼一看，啊！  
`from Dbutils.pooled_db import PooledDB`  
里的"Dbutils"里的"D"不是大写！  
再去官方开发文档确认一下  
完蛋，确实是我错了，马上改成小写的"d"：  
`from dbutils.pooled_db import PooledDB`  
修复BUG，然后为了以防万一，我还直接复制粘贴他的这行代码  
确保万无一失。。。  
看来Visual Studio Code查看导入包可以忽略大小写不匹配的情况  
直接打开源文件，这或许算是个BUG。。。  

代码跑通了。。  

```powershell
PS E:\Data\project\2020_MyBigData\MyBigData_Python3>  & 'C:\Program Files\Python38\python.exe' 'E:\sysdata\xfl666\.vscode\extensions\ms-python.python-2020.12.424452561\pythonFiles\lib\python\debugpy\launcher' '45318' '--' 'e:\Data\project\2020_MyBigData\MyBigData_Python3\testSQL.py'
(1, 666)
(233, 678)
```

重新整理了一下学习log，因为之前学习的时候并没有做跟踪记录  
后来重新再走一遍学习过程写出来的，文章顺序不自然  
（因为躺了坑之后，把坑填平了，然后又忘记是怎么被坑的，XD）  

我发现这篇博客 <https://www.cnblogs.com/jiangxiaobo/p/12786205.html>  
开始写得还好，具有引导性，到后面我仔细想了想  
我们需要的是 **单例模式** 的连接池，不然多线程会有海量的内存开销  
然而………作者把它写成了一个类，这就挺迷的……  
如果以模块的形式导入到其它Python文件，据说可以保证是单例  
但是写成一个类难道不是多此一举？  
不懂唉，先暂时瞎搞吧。。直接给它脱掉class的外衣  

于是我索性简化了一番，把他的 **db_dbutils_init.py** 直接删掉了，  
**mysqlhelper.py** 我觉得也是留不了多久了，现在它的用处就只有参考学习  

突然想搞个数据库连接池monitor监视器，  
因为觉得数据不透明带给人的安全感是直线下滑的  

**ten thousand years later**

停止继续开发这个项目2个星期了。。  
失踪人口回归了！！  
可能有些网友会问：“干啥去了？”  

事情的发展是这样的：  
思考，怎么搞个监视器（监控表盘）？  
这种东西。。肯定是多线程的，而且不能阻塞主线程  
（主线程也可以叫祖线程吧？可以这样称呼吧。。），  
因为只有原始线程继续运行，才会产生数据啊！！  
所以又要递归式学习怎么搞Python多线程？  
然后百度搜索“Python3 多线程”  
去了 “runoob.com 菜鸟教程”学习了一下“threading”  
发现有点难搞，貌似主线程还会阻塞子线程的，  
这不符合我的要求。。  
然后我在打工之余，左思右想，突然灵光乍现！！  
我可以直接搜索烂大街的“Python3 多线程下载器”，  
不就可以直接参考借鉴了？  
而且因为是成品，还可以直接测试，免掉趟坑过程，  
或者减少趟坑时间（有可能代码有问题，依然会栽大跟头），  
不管怎么说，这是一种极佳的学习模式。  

因为最近私人鸡场套Cloudflare CDN番茄出国龟速，  
需要手动遴选CDN高速节点，每天高速CDN节点都会变化  
每天都需要手动修改配置，太麻烦了。。  
于是我去开发了另一个项目——"Cloudflare better node"  
目前还没发布到GitHub，因为还没开发好。  
我的目标是使用Python3实现全自动的CDN遴选、测速  
并即时更新DNSPOD的DNS记录，  
从而实现某ray番茄工具的配置文件不变化，  
却可以让它跑最快CDN节点。  
其中遴选是基于下载测速的，需要使用到多线程下载技术。  
所以正好学习练手一番，这个……就不在这里记录了。。  
期待一波吧。(^▽^)  

2021年6月1日，失踪人口回归！  
网友：Cloudflare better node搞好了没有？终于记得回来开发MyBigData项目了？  
弱小可怜又无助的我：开发好了开发好了，MyBigData在做了在做了，唉。。。  

Cloudflare better node项目是一个简单的用Python3.8脚本写的无脑测速工具  
开源项目地址：<https://github.com/xfl12345/cloudflare-better-node>  

