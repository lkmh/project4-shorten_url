from redis_connect import redis_connection as r

print(r.get(123123).decode('UTF-8'))

def redis_check_if_exist(redis_key):
    if r.exists(redis_key) == 0:
        return False 
    return True

def redis_get(redis_key):
    data = r.get(redis_key).decode('UTF-8')
    return data

def redis_store(redis_key, redis_value):
    r.set(redis_key, redis_value)
    return True 
    