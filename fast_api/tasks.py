from redis import Redis
from rq import Queue 


conn = Redis(host='localhost', port=6379)
queue = Queue(connection=conn)

def send_hello(hello:str):
    return {"status": "done", "message": hello}   