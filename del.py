import redis
r = redis.Redis(host='localhost', port=6379, db=0)
db_keys = r.keys(pattern="*")
print((len(db_keys)))
for single in db_keys:    
    chat_id = r.delete(single).decode("UTF-8")
    print(single.decode("UTF-8"), ": ", chat_id)
