import re

ONE_BIN_KB: int = 1024  # 2^10
ONE_BIN_MB: int = 0x100000  # 2^20
ONE_BIN_GB: int = 0x40000000  # 2^30
ONE_BIN_TB: int = 0x10000000000  # 2^40
ONE_BIN_PB: int = 0x4000000000000  # 2^50

ONE_OF_1024: float = 0.0009765625  # 1/1024

# 正则表达式匹配 （没错，又在重复造轮子了，我就是从惨不忍睹的毕业设计里直接copy过来的）
# 源码：https://github.com/xfl12345/jsp_netdisk/blob/main/src/main/java/com/github/xfl12345/jsp_netdisk/model/utility/MyStrIsOK.java
matchLetterAndDigitOnly = "^[a-z0-9A-Z]+$"
matchLetterOnly = "^[a-zA-Z]+$"
matchDigitOnly = "^[0-9]+$"
matchNumWithSignOnly = "[+-]?[1-9]+[0-9]*(\\.[0-9]+)?"
matchEmailOnly = "([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+"
matchFilename = "[^\\s\\\\/:\\*\\?\\\"<>\\|](\\x20|[^\\s\\\\/:\\*\\?\\\"<>\\|])*[^\\s\\\\/:\\*\\?\\\"<>\\|\\.]$"
# TODO 把match only相关的正则表达式 写成 re.compile 以便后续开发直接用
containUppercaseLetter = re.compile("[A-Z]")
containLowercaseLetter = re.compile("[a-z]")
containLetter = re.compile("[a-zA-Z]")
containNum = re.compile("\\d")
containLetterAndDigit = re.compile("[a-z0-9A-Z]")
# 匹配如下特殊符号
# ( ) ` ~ ! @ # $ % ^ & * - _ + = | { } [ ] : ; ' < > , . ? /
containAllowedSpecialCharacter = re.compile("[`~!@#$%^&*()+=|{}':;,\\[\\].\\\\<>/?—]")
# 匹配UTF8编码的汉字
containChineseInUTF8 = re.compile("[\u4e00-\u9fa5]")
