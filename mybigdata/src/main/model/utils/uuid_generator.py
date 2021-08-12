import os
import time
import random
import uuid
import threading


# def uuid1():
#   lock.acquire() # 获得锁
#   uuid_item = uuid.uuid1()
#   lock.release() # 释放锁
#   return uuid_item

class MyUUID(object):
    def __init__(self):
        self.lock = threading.Lock()
        # 获取进程ID
        pid = os.getpid()
        # 获取当前对象在内存里的虚拟ID
        python_obj_id = id(self)
        # 获取当前线程标识ID
        curr_thread_ident = threading.get_ident()
        # 生成自定义 16位 的 标识ID（区分度越高，真随机性越好）
        self.my_ident = ((curr_thread_ident + (python_obj_id << 4) + (pid << 8)) & 0xFFFF)
        self._last_timestamp = time.time_ns() // 100 + 0x01b21dd213814000

    def uuid1(self, node=None, clock_seq=None):
        self.lock.acquire(blocking=True)
        nanoseconds = time.time_ns()
        self.lock.release()
        # 0x01b21dd213814000 is the number of 100-ns intervals between the
        # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
        timestamp = nanoseconds // 100 + 0x01b21dd213814000
        if self._last_timestamp is not None and timestamp <= self._last_timestamp:
            timestamp = self._last_timestamp + 1
        self._last_timestamp = timestamp
        if clock_seq is None:
            clock_seq = (random.getrandbits(8) + self.my_ident) & 0x7FFF
            # clock_seq = random.getrandbits(14)  # instead of stable storage
        time_low = timestamp & 0xffffffff
        time_mid = (timestamp >> 32) & 0xffff
        time_hi_version = (timestamp >> 48) & 0x0fff
        clock_seq_low = clock_seq & 0xff
        clock_seq_hi_variant = (clock_seq >> 8) & 0x3f
        if node is None:
            node = uuid.getnode()
        return uuid.UUID(fields=(time_low, time_mid, time_hi_version,
                                 clock_seq_hi_variant, clock_seq_low, node), version=1)


UUID_GENERATOR = MyUUID()
