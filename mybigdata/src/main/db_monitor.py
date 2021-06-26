from mybigdata.src.main import my_pooled_db

import flask
import flask_restful
import threading
import tkinter as tk


class Monitor(flask_restful.Resource):
    the_pool = None

    def __init__(self):
        self.the_pool = my_pooled_db.connection_pool

    def get(self):
        response_data = {}
        if hasattr(self.the_pool, "_connections"):
            response_data["connections_count"] = self.the_pool._connections
        if hasattr(self.the_pool, "_shared_cache"):
            response_data["shared_cache_count"] = len(self.the_pool._shared_cache)
        if hasattr(self.the_pool, "_idle_cache"):
            response_data["idle_cache_count"] = len(self.the_pool._idle_cache)
        return flask.make_response(response_data)



# 还没码好，千万别运行哦！
class MyTkinterWatcher(threading.Thread, Monitor):
    root = None
    ui_h = 800;  # 输出画面的高度(px)
    ui_w = 600;  # 输出画面的宽度(px)
    connections_text_ui = None
    shared_cache_text_ui = None
    idle_cache_text_ui = None

    def __init__(self):
        '''Init frame
        '''
        threading.Thread.__init__(self)
        self.root = tk.Tk()
        self.center_window(w=self.ui_w)
        self.connections_text_ui = tk.Label(self.root, \
                                            foreground="blue", text="")
        self.connections_text_ui.pack()
        self.root.mainloop()

    def run(self):
        while True:
            self.connections_text_ui['text'] = \
                str(len(Monitor.the_pool._connections))

    def center_window(self, w=800, h=600):
        # get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        # 设置窗口大小以及左上角的位置  WIDTHxHEIGHT+X+Y
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
