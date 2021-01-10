import my_pooled_db

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

    
