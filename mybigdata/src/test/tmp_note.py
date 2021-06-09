
num = (1 << 64) -1

ONE_YEAR_TIME = 60 * 60 * 24 * 365

print("一年时间约有 " + str(ONE_YEAR_TIME) + "秒")

peer_sec = int(num / (ONE_YEAR_TIME * 1000))

print("若千年之内消耗掉64位无符号整型，则平均每秒需消耗 " + str(peer_sec) + "个数字")