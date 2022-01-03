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

因为前段时间在忙毕业设计，我的毕业设计是搞了个基于SSM框架的JavaWeb网盘，  
里面就大规模使用JSON作为请求和响应的格式，而且是全方面的统一  
（除了上传和下载文件，其它API都使用JSON）  
然后想想API怎么设计，以及怎么样才能不会被SQL注入。  
其实没什么麻烦的，就是折腾个JSON Schema验证一下JSON数据是否合法就可以了！  
Role A:你可真睿（鸡）智（贼）！  
Role B:哈哈！那当然！  

截止到目前，我在GitHub上面看到一篇 **Readme** 推荐了这些东西：  

* [jsonschema](https://github.com/Julian/jsonschema)
* [fastjsonschema](https://github.com/seznam/python-fastjsonschema)
* [hypothesis-jsonschema](https://github.com/Zac-HD/hypothesis-jsonschema)
* [jschon](https://github.com/marksparkza/jschon)

网址附上：<https://github.com/json-schema-org/JSON-Schema-Test-Suite>

然后我选用了 **jschon** 作为轮子，只因为它更新频率高些  
巴拉巴拉写了一堆测试代码，确认可用（实际上是自己太菜，在那练手）  

想了想，这个MyBigData项目应该开发一些轮子给大家用，  
实现完全傻瓜式地使用MySQL数据库（其它数据库以后再说）  

然后怎么设计这个轮子呢？……  
没错，依然是使用JSON作为模型，实现JSON -> MySQL table的转换  
因为JSON可读性很强，而且还可以借用JSON Schema校验数据过滤一部分SQL注入，  
所以我觉得这个思路没有什么问题（甚至还有点优秀）。。。  

如何开发这个轮子呢？  
先把HTTP API折腾出来再说吧，否则动态测试有点困难。。  

为了避免重复造轮子，选择一下现成的Web框架  

斟酌损益，最终敲定选择使用flask  
因为它轻量易学，主要是因为轻量（说不定可以跑在 newifi D2 那种垃圾机器上）  

二话不说，就是开干！  

```shell
pip install flask flask-restful
pip install --upgrade flask flask-restful
```

隔了 一个星期 才突然想起来更新学习日志  
却发现自学了太多东西，没做记录，也忘记了自己是如何“面向搜索引擎编程”的  
flask框架 和 flask-restful框架……这个这个……我是怎么入门的呢？  

flask框架……我是先看官方开发文档入门的，网址如下：  
<https://dormousehole.readthedocs.io/en/latest/quickstart.html>  

flask-restful框架…… 参考学习了一下技术博客 <https://www.jianshu.com/p/6ac1cab17929>  
简单地入了一下门，但是深入使用这种强大的框架是远远不够的，于是找了一下官方开发文档  
首先去Python pip软件源 <https://pypi.org/> 搜索 "**Flask-RESTful**"  
然后来到了 <https://pypi.org/project/Flask-RESTful/>  
根据左边的GitHub仓库被Star的个数，找到了官方GitHub仓库  
<https://github.com/flask-restful/flask-restful>  
然后在官方GitHub仓库的 "**About**" 简介中，找到了官方指定的开发文档  
<http://flask-restful.readthedocs.io/>  
然后就可以“愉快地”使用机器翻译，推敲文章意思，边学习英语边自学flask-restful  
（也是后来才发现，前面关于 flask-restful框架 的技术博客里的源代码，原来直接源自官方开发文档！）  

然后就是照葫芦画瓢地用flask-restful框架做了一个Web API，完成 数据库连接池 的监视器功能  

后面大量学习了一下关于MySQL的引索及性能优化。。  
这个知识点太多，非常零碎，犯懒癌又不想码字了  
（真的太多了，又一次恨不得这个项目马上可以投入使用，全自动地把学习轨迹记录下来）  

整理一下数据库插入数据的顺序……  

首先假定字符串全部都在 **string_content** 表里，但是 每一条数据都必须有一个 **global_id**  
若 **string_content** 表里的每一行数据都要有一个 **data_format** ，  
而 **data_format** 是一个自环引用，引用自己表里的主键ID——**string_id**  
则第一条字符串必须是用来描述 **data_format** 的……  

为了保证初始化的数据可以正常插入，则不能在建表的同时添加外键约束，只能先斩后奏  
故优先创建  **string_content** 表，然后往 **string_content**表 插入  
**global_data_record** 表里的关于 **string_content**表 的 必填字段对应的值。  

后来想想 **string_id** 太过局限， **global_id** 失去意义。。。  
干脆整个 数据库实例 里面只保留 **global_id** 这一条自增主键。  
这样不会破坏原有设计原则 同时 逻辑也通顺了！（果然正确的答案，往往比较简单粗暴）  

巴拉巴拉又写了一堆东西，总算是狠下心来把 JSON Schema 折腾上了  
Role A:学习日志断片太严重了，楼主，你不填坑吗？  
Role B:我也不想这样啊，但我实在补不来了。。。（逃）   

折腾了一堆东西，究竟在折腾什么玩意？  
后来发现学习、研究这两件事，都是得step by step的，  
急不来，急不来，先打草稿再码code，否则事倍功半。  
那么，究竟是遇到什么问题卡住了呢？  
那就是：  
1. **MyBigData** 如何优雅地设计成可以通过配置文件来配置？  
2. **MyBigData** 如何知道JSON的六种值的类型存放到数据库的哪些表里？  

后来遵照不知道从哪来的“解耦思想”，开始模仿 **MyBatis** 的模式，  
想把所有配置相关的东西放到文件里！  
当然，还得是 **JSON格式** 存储配置，用 **JSONSchema** 去检查是否存在错误  
然后 **MyBigData** 通过读取配置文件得知JSON的六种值的类型  
应该存放到数据库的哪些表里。  
后来因为留给我连续开发 **MyBigData** 的时间并不多，  
所以写SQL语句的时候，干脆直接硬编码拼接字符串，一路高歌猛进。  
但后来想想，需要折腾复杂查询的时候，这种写法绝对是灾难。。  

于是还是去找了一下Python的 **ORM框架** 。  
选择的余地并不多，只能说，要挑，还只能挑主流的。  
毕竟太冷门的，对后来参与开发的开发者非常不友好。而且开发文档说明可能也很少，  
也很可能缺乏技术支持，对我这个只想求快速开发的小笨蛋来说，非常不利。  

因为抛弃了Django，所以 **DjangoORM** 就不纳入考虑了。  
剩下两个入围选手：**SQLAlchemy** 和 **SQLObject**  

当我发现 **SQLAlchemy** 提供了相当多的API，是个非常强悍的ORM框架，  
而且相当多的人在使用，我觉得我应该学习 **SQLAlchemy** 。直到初步了解后，  
我发现我不得不弃用它。  

网友A：话别说一半啊，说明白为啥弃用 SQLAlchemy 啊？  
随时会猝死的作者：因为学习成本太高，它自带了连接池  
对我已有的 DBUtils 模块产生冲突  
（要么 DBUtils ，要么 SQLAlchemy ，做选择吧！）。  
如果选用 **SQLAlchemy** ，  
那么将会导致已有的大量代码都是多余的。其实这可能都不算什么，最要命的是  
**SQLAlchemy** 似乎 **不允许** 你去 **动态地** 修改表的结构！！！  
在我几经尝试修改已有的 Mapper 对象里的 表名 时，  
**SQLAlchemy** 总是给我报错！！  

我已经确认我找了无数遍 StackOverFlow ，  
但发现他们都是曲线救国地新建一个 Mapper ，然后注册到内存里面去。  
可我想在加载配置文件时动态地设置 表名 ，并让旧的 Mapper 从内存里删除掉，  
这样才不会导致后续用户动态地新建一个曾经用过的表名时失败。  
**SQLAlchemy** 这种固化机制，基本可以说，和 **MyBigData** 玩完。  

后来再看到有人在 **知乎** 评论说道：  
[https://www.zhihu.com/question/27551008/answer/68916625](https://www.zhihu.com/question/27551008/answer/68916625)  
"一些别的ORM，比如Hibernate，会提供自动更新schema的方式。  
但是SQLAlchemy不会，它本身没有提供修改表结构（schema）的方式。"  
——X1angLi  

很好，纵使 **SQLAlchemy** 再NB，只要还是限制得这么死，  
那就无缘 **MyBigData** 。  
（也可以松口气了。毕竟不需要再花很长时间去学习、迁就 **SQLAlchemy** 了）  

那就 **SQLObject** ？  

后来我又了解到，有另一种框架——**PeeWee**  

因为工作原因，导致项目停更了6个月之久！！！  
可能有人会问：国庆7天干嘛去了？  
社畜本人：问得好！因为公司只放了4天假！而且项目的部署需要硬件支持！  
然后在国庆之前准备了东芝10TB NAS专用硬盘、联想粒子云SS1（硬改2GB内存版）  
回到老家重新刷机、部署完机器后，又继续开展“百度网盘搬家”大战……  
把第三方云端所有文件迁移回本地，一方面是为了数据安全、MyBigData功能试验，  
另一方面就是打算 2022年 不再续费百度网盘年度会员！！！  
这个迁移老折腾了，因为百度网盘并没有释放支持 **armbian** 系统可用的客户端。  
所以是用了 **x86** 架构的笔记本电脑配合 **FileZilla** 怼粒子云上的 **sftp**  来进行。  
后来发现网盘上的小文件非常多，2天下载时间根本不够耗！  
然后2天时间用于往返老家和深圳……  
回到深圳了怎么办？先后尝试了各种利用百度云API的第三方开源客户端。  
Go语言版的、Python版的，都不行。都不可靠，下载下载着就失败了。  
容易发生部分文件未下载的问题，速度还不够稳定……  
都开了会员了，还这体验。可以说，百度网盘是真的恶心。  
后来我又买了矿渣机器（x86架构的）锐角云来挂机下载，历时10天，  
终于从百度网盘下载完 **2TiB** 的文件并远隔几百公里，走IPv6网络，把数据从深圳上传回老家！！！  
（中国移动是真的辣鸡，600Mbps下行的宽带，居然只给30Mbps上行！？）  

**PeeWee** 这个 **ORM框架** 限制得很少，自由度非常大！  
配合各种炫酷的hack拓展，已经完全可以胜任 **MyBigData** 的  
额外需求——可对 **表** 进行新增、删除 和 修改！  

项目许久未动，很多东西早忘了。于是重新阅读源码，添加了些许注释……  
然后苦逼地到了星期一，又要上班！元旦法定节假日人家都3天的，我只有2天！  
真的是又一次实锤社畜身份……于是又要停更一阵子了！春节见！  
