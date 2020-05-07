from CoolModule import Worker, Tasker
import time
import threading

tasks = Tasker(dbname='TaskDB',host='localhost',password = 'passwd',port='5433',user='postgres',threaded=True)
tasks.init()
with open('internet.txt','r',encoding='utf-8') as f:
    tasks.start(f.readlines())
name = Worker(dbname='TaskDB',host='localhost',password = 'passwd',port='5433',user='postgres')
name.listen(threaded=True)
time.sleep(20)
name.stop()