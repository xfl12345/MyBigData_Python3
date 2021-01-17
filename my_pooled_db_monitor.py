from typing import Text
import my_pooled_db
import threading
import tkinter as tk
import tkinter.messagebox
import random
import time

# 还没码好，千万别运行哦！
class monitor:
    the_pool = None
    _running = True

    def __init__(self):
        self.the_pool = my_pooled_db.connection_pool
        self._running = True
        

    def run(self,**arg):
        while(self._running):
            print("connections count=",len(self.the_pool._connections))
            print("shared_cache count=",len(self.the_pool._shared_cache))
            print("idle_cache count=",len(self.the_pool._idle_cache))

    def stop(self):
        self._running = False

    
class my_tkinter_watcher(threading.Thread, monitor):
    root = None
    ui_h = 800; # 输出画面的高度(px)
    ui_w = 600; # 输出画面的宽度(px)
    connections_text_ui = None
    shared_cache_text_ui = None
    idle_cache_text_ui = None

    def __init__(self):
        '''Init frame
        '''
        threading.Thread.__init__(self)
        self.root = tk.Tk()
        self.center_window(w = self.ui_w)
        self.connections_text_ui = tk.Label(self.root,\
             foreground="blue", text="" )
        self.connections_text_ui.pack()
        self.root.mainloop()

    def run(self):
        while True:
            self.connections_text_ui['text'] = \
                str(len(monitor.the_pool._connections))
    
    def center_window(self,w=800, h=600):
        # get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        #设置窗口大小以及左上角的位置  WIDTHxHEIGHT+X+Y
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    
