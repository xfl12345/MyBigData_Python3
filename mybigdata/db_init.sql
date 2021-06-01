/**
* Source Server Type    : MySQL
* Source Server AppInfo : 5.7.26
* Source Host           : 127.0.0.1:3306
* Source Schema         : xfl_mybigdata
* FileOperation Encoding         : utf-8
* Date: 2021/4/6 22:26:19
*/

create
database xfl_mybigdata DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

use
xfl_mybigdata;

SET
FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS `test_table` (
  `ID` int(11) NOT NULL,
  `num` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `test_table` (`ID`, `num`) VALUES
(1, 666),
(233, 678);

SET
FOREIGN_KEY_CHECKS = 1;