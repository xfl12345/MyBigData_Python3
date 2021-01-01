import my_pooled_db

the_pool = my_pooled_db.connection_pool
while(True):
    print("connections count=",len(the_pool._connections))
    print("shared_cache count=",len(the_pool._shared_cache))
    print("idle_cache count=",len(the_pool._idle_cache))

    
