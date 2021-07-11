import concurrent.futures as ccfutures
import time

import mybigdata.src.main.model.utils.uuid_generator as uuid_generator
# from mybigdata.src.test.test import producer


def producer():
    my_uuid = uuid_generator.MyUUID()
    uuid_one = my_uuid.uuid1()
    for i in range(50000):
        print(my_uuid.uuid1())

if __name__ == '__main__':

    my_uuid = uuid_generator.MyUUID()
    uuid_one = my_uuid.uuid1()
    print(uuid_one)
    print(uuid_one.is_safe)
    print()

    p_pool = ccfutures.ThreadPoolExecutor(max_workers=5)
    start_time = time.time()
    for i in range(5):
        p_pool.submit(producer, )
    p_pool.shutdown(wait=True)
    stop_time = time.time()
    print("总共耗时：" + str(stop_time - start_time) + " 秒")
