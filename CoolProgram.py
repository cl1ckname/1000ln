from CoolModule import worker, tasker
import time

tasks = tasker(dbname='TaskDB',host='localhost',password = 'passwd',port='5433',user='postgres',threaded=True)
tasks.init()
with open('internet.txt','r',encoding='utf-8') as f:
    tasks.start(f.readlines())
    time.sleep(10)
    tasks.stop()
name = worker(dbname='TaskDB',host='localhost',password = 'passwd',port='5433',user='postgres')
name.listen()