/**
* Source Server Type             : MySQL
* Source Server AppInfo          : 5.7.26
* Source Host                    : 127.0.0.1:3306
* Source Schema                  : xfl_mybigdata
* FileOperation Encoding         : utf-8
* Date: 2021/6/9 17:00:00
*/

# drop database xfl_mybigdata

create
    database xfl_mybigdata DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

use
    xfl_mybigdata;

SET
    FOREIGN_KEY_CHECKS = 0;

CREATE TABLE `test_table`
(
    `ID`  int NOT NULL PRIMARY KEY,
    `num` int NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

INSERT INTO `test_table` (`ID`, `num`)
VALUES (1, 666),
       (233, 678);


# 优先创建 字符串记录表 ，毕竟 全局ID记录表 对 字符串表 存在必要依赖
/**
  一个庞大的 字符串记录表，暂时还没做来源系统
 */
CREATE TABLE string_content
(
    `global_id`      bigint unsigned not null comment '当前表所在数据库实例里的全局ID',
    `data_format`    bigint unsigned comment '字符串结构格式',
    `content_length` smallint        not null default -1 comment '字符串长度',
    `string_content` varchar(16000)  not null comment '字符串内容，最大长度为16000个字符',
    unique key unique_global_id (global_id) comment '确保每一行数据对应一个相对于数据库唯一的global_id',
    index boost_query_id (data_format, content_length) comment '加速查询主键，避免全表扫描',
    index boost_query_string_content (string_content(768)) comment '尽量加速检索字符串内容，尤其是短字符串'
) AUTO_INCREMENT = 65536
  ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;

INSERT INTO string_content (global_id, data_format, string_content)
       # 第一个字符串，关于数据格式——text
values (1, 1, 'text'),
       # 第二个字符串，是一个空字符串
       (2, 1, ''),
       # 第三个字符串，关于 "描述" 本身
       (3, 1, '说明、描述'),
       # 第四个字符串，关于 第一个字符串 的描述
       (4, 1, '一种字符串内容格式'),
       # 第五个字符串，关于 字符串表 的名称
       (5, 1, '字符串记录表的名称'),
       # 第六个字符串，关于 字符串表 的名称
       (6, 1, 'string_content'),
       # 第七个字符串，关于 全局ID记录表 的描述
       (7, 1, '全局ID记录表的名称'),
       # 第八个字符串，关于 全局ID记录表 的名称
       (8, 1, 'global_data_record');


/**
  全局ID记录表，记录并关联当前数据库内所有表的每一行数据
 */
CREATE TABLE global_data_record
(
    `global_id`      bigint unsigned not null PRIMARY KEY AUTO_INCREMENT comment '当前表所在数据库实例里的全局ID',
    `uuid`           char(36)        not null comment '关于某行数据的，整个MySQL数据库乃至全球唯一的真正的全局ID',
    `create_time`    datetime        not null DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    `update_time`    datetime        not null DEFAULT CURRENT_TIMESTAMP comment '修改时间',
    `modified_count` bigint unsigned not null default 1 comment '修改次数（版本迭代）',
    `table_name`     bigint unsigned not null comment '该行数据所在的表名',
    `description`    bigint unsigned not null default 2 comment '该行数据的附加简述',
    # 全局ID 记录表，删除乃大忌。拒绝一切外表级联删除行记录，只允许按 global_id 或 uuid 删除行记录
    # 遵循 一切普通文本 由 字符串记录表
    foreign key (table_name) references string_content (global_id) on delete restrict on update cascade,
    foreign key (description) references string_content (global_id) on delete restrict on update cascade,
    unique key index_uuid (uuid) comment '确保UUID的唯一性',
    index boost_query_all (uuid, create_time, update_time, modified_count, table_name, description)
) AUTO_INCREMENT = 65536
  ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;

INSERT INTO global_data_record (global_id, uuid, table_name, description)
# 先斩后奏 之 关联已有的 字符串 数据
VALUES (1, 'f5ad7c01-cb7a-11eb-8b78-f828196a1686', 6, 4),
       (2, 'f5ad7c02-cb7a-11eb-b03f-f828196a1686', 6, 2),
       (3, 'f5ad7c03-cb7a-11eb-ac6f-f828196a1686', 6, 3),
       (4, 'f5ad7c04-cb7a-11eb-8173-f828196a1686', 6, 3),
       (5, 'f5ad7c05-cb7a-11eb-a0a1-f828196a1686', 6, 3),
       (6, 'f5ad7c06-cb7a-11eb-af85-f828196a1686', 6, 5),
       (7, 'f5ad7c07-cb7a-11eb-ad01-f828196a1686', 6, 3),
       (8, 'f5ad7c08-cb7a-11eb-bf48-f828196a1686', 6, 7);

# 为 字符串表 添加 全局ID 约束
alter table string_content
    add foreign key (global_id) references global_data_record (global_id) on delete cascade on update cascade;

/*
SELECT
    g.global_id,
    g.uuid,
    g.create_time,
    g.update_time,
    g.modified_count,
    table_name_src.string_content AS `table_name`,
    description_src.string_content AS `description`,
    item_data.string_content AS `data`
FROM
    global_data_record AS g,
    string_content AS table_name_src,
    string_content AS description_src,
    string_content AS item_data
WHERE
    table_name_src.global_id = g.table_name
    AND  description_src.global_id = g.description
    AND item_data.global_id = g.global_id
 */

# 来个插入数据的正规流程示范
# 先向 global_data_record 表注册，通过查询 UUID 拿到 global_id


# 注册 table_schema_record 表
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (9, 'f5ad7c09-cb7a-11eb-83ea-f828196a1686', 6, 3);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (9, 1, 'table-JSON模板记录表的名称');
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (10, 'f5ad7c0a-cb7a-11eb-ac82-f828196a1686', 6, 9);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (10, 1, 'table_schema_record');

# 注册 tree_struct_record 表
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (11, 'f5ad7c0b-cb7a-11eb-9265-f828196a1686', 6, 3);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (11, 1, '专门记录树状结构的表的名称');
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (12, 'f5ad7c0c-cb7a-11eb-aaed-f828196a1686', 6, 11);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (12, 1, 'tree_struct_record');

# 注册 binary_relationship_record 表
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (13, 'f5ad7c0d-cb7a-11eb-8151-f828196a1686', 6, 3);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (13, 1, '专门记录二元关系的表的名称');
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (14, 'f5ad7c0e-cb7a-11eb-9ac5-f828196a1686', 6, 13);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (14, 1, 'binary_relationship_record');

# 注册 group_record 表
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (15, 'f5ad7c0f-cb7a-11eb-90bf-f828196a1686', 6, 3);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (15, 1, '组号记录表的名称');
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (16, 'f5ad7c10-cb7a-11eb-9220-f828196a1686', 6, 15);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (16, 1, 'group_record');

# 注册 group_content 表
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (17, 'f5ad7c11-cb7a-11eb-85ff-f828196a1686', 6, 3);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (17, 1, '组成员记录表的名称');
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (18, 'f5ad7c12-cb7a-11eb-be7b-f828196a1686', 6, 17);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (18, 1, 'group_content');

# 注册 label_record 表
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (19, 'f5ad7c13-cb7a-11eb-a63c-f828196a1686', 6, 3);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (19, 1, '标签记录表的名称');
INSERT INTO global_data_record (global_id, uuid, table_name, description)
VALUES (20, 'f5ad7c14-cb7a-11eb-b818-f828196a1686', 6, 19);
INSERT INTO string_content (global_id, data_format, string_content)
VALUES (20, 1, 'label_record');



# 补完字符串长度
UPDATE string_content
SET content_length = CHAR_LENGTH(string_content)
WHERE content_length = default(content_length);

/**

f5ad7c15-cb7a-11eb-b7f9-f828196a1686
f5ad7c16-cb7a-11eb-a43e-f828196a1686
f5ad7c17-cb7a-11eb-b27a-f828196a1686
f5ad7c18-cb7a-11eb-92b6-f828196a1686
f5ad7c19-cb7a-11eb-bbc6-f828196a1686
f5ad7c1a-cb7a-11eb-a61c-f828196a1686
f5ad7c1b-cb7a-11eb-808d-f828196a1686
f5ada312-cb7a-11eb-9f9c-f828196a1686
f5ada313-cb7a-11eb-8316-f828196a1686
f5ada314-cb7a-11eb-bf32-f828196a1686
 */

/**
  MyBigData 特色功能之一，就是使用JSON Schema完成对MySQL模板化操作
  这个表主要存放JSON模板
 */
CREATE TABLE table_schema_record
(
    `global_id`      bigint unsigned not null comment '当前表所在数据库实例里的全局ID',
    `schema_name`    bigint unsigned not null comment '插表模板名称',
    `content_length` smallint        not null default -1 comment 'json_schema 字段的长度',
    # 这里不遵循 “一切普通文本 由 字符串记录表” 的原则
    # 是因为json格式的字符串可以使用json格式存储，MySQL原生支持JSON格式
    # 暂不考虑使用JSON格式存储JSON字符串，暂且先保留修改空间
    `json_schema`    varchar(16000)  not null comment '插表模板',
    foreign key (global_id) references global_data_record (global_id) on delete cascade on update cascade,
    unique key unique_global_id (global_id) comment '确保每一行数据对应一个相对于数据库唯一的global_id',
    unique key index_schema_name (schema_name) comment '确保插表模板名称的唯一性',
    index boost_query_id (global_id, schema_name, content_length) comment '加速查询主键，避免全表扫描'
) AUTO_INCREMENT = 65536
  ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;

/**
  专门记录树状结构的表
 */
CREATE TABLE tree_struct_record
(
    `global_id`      bigint unsigned not null comment '当前表所在数据库实例里的全局ID',
    `root_id`        bigint unsigned not null comment '根节点对象',
    `item_count`     int unsigned    not null comment '整个树的节点个数',
    `tree_deep`      int unsigned    not null comment '整个树的深度（有几层）',
    `content_length` smallint        not null default -1 comment 'JSON文本长度',
    # 暂不考虑使用JSON格式存储JSON字符串，且先保留修改空间
    `struct_data`    varchar(16000)  not null comment '以JSON字符串形式记载树形结构',
    foreign key (global_id) references global_data_record (global_id) on delete cascade on update cascade,
    unique key unique_global_id (global_id) comment '确保每一行数据对应一个相对于数据库唯一的global_id',
    foreign key (root_id) references global_data_record (global_id) on delete cascade on update cascade,
    index boost_query_id (global_id, root_id, item_count, tree_deep, content_length) comment '加速查询主键，避免全表扫描'
) AUTO_INCREMENT = 65536
  ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;

/**
  专门记录二元关系的表
 */
CREATE TABLE binary_relationship_record
(
    `global_id`              bigint unsigned not null comment '当前表所在数据库实例里的全局ID',
    `item_a`                 bigint unsigned not null comment '对象A',
    `item_b`                 bigint unsigned not null comment '对象B',
    foreign key (global_id) references global_data_record (global_id) on delete cascade on update cascade,
    unique key unique_global_id (global_id) comment '确保每一行数据对应一个相对于数据库唯一的global_id',
    foreign key (item_a) references global_data_record (global_id) on delete cascade on update cascade,
    foreign key (item_b) references global_data_record (global_id) on delete cascade on update cascade,
    unique unique_limit_ab (item_a, item_b) comment '不允许出现重复关系，以免浪费空间',
    unique unique_limit_ba (item_b, item_a) comment '不管是正着来，还是反着来，都不允许出现重复关系，以免浪费空间',
    index boost_query_all (global_id, item_a, item_b) comment '加速查询全部数据'
) AUTO_INCREMENT = 65536
  ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;

/**
  专门记录 “组” 的表
  不过这 group_record 表只记组号
 */
CREATE TABLE group_record
(
    `global_id` bigint unsigned not null comment '当前表所在数据库实例里的全局ID',
    `group_name` bigint unsigned not null default 2 comment '组名',
    foreign key (global_id) references global_data_record (global_id) on delete cascade on update cascade,
    unique key unique_global_id (global_id) comment '确保每一行数据对应一个相对于数据库唯一的global_id',
    index boost_query_all (global_id, group_name) comment '加速查询全部数据'
) AUTO_INCREMENT = 65536
  ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;

/**
  专门记录 “组” 的表，所有关于“列表（一维数组）”、“集合”和“分组”等概念的数据的 关系 都记录于该表
 */
CREATE TABLE group_content
(
    `group_id` bigint unsigned not null comment '组id',
    `item`     bigint unsigned not null comment '组内对象',
    # 关联 group_record 表。毕竟 “组” 这种概念，本就是一对多的关系。
    foreign key (group_id) references group_record (global_id) on delete cascade on update cascade,
    foreign key (item) references global_data_record (global_id) on delete cascade on update cascade,
    index boost_query_all (group_id, item) comment '加速查询全部数据'
) ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;


/**
  专门记录 “标签” 的表——标签记录表
 */
CREATE TABLE label_record
(
    `global_id`  bigint unsigned not null comment '当前表所在数据库实例里的全局ID',
    `label_name` bigint unsigned not null comment '标签名',
    `group_item` bigint unsigned not null comment '被贴标签的对象集合',
    foreign key (global_id) references global_data_record (global_id) on delete cascade on update cascade,
    unique key unique_global_id (global_id) comment '确保每一行数据对应一个相对于数据库唯一的global_id',
    # 拒绝一切外表级联删除行记录，只允许按 主键id 删除行记录
    foreign key (label_name) references string_content (global_id) on delete restrict on update cascade,
    foreign key (group_item) references group_record (global_id) on delete restrict on update cascade,
    index boost_query_all (label_name, group_item) comment '加速查询全部数据'
) AUTO_INCREMENT = 65536
  ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = Dynamic;

/**
  暂时还没写完，因为发现了很多问题欠缺考虑
 */


SET
    FOREIGN_KEY_CHECKS = 1;