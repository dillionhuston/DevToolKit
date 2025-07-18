from celery import Celery

celery_app = Celery(
    'worker',
    broker='redis://localhost:6379/0',   
    backend='redis://localhost:6379/0', #fallback
    include=['tasks']  
)

@celery_app.task(name="tasks.add")
def add(x, y):
    return x + y