import psycopg2
import time
import logging
import threading

class tasker():

    
    def __init__(self, dbname, user, password, host, port, periodicity=3, threaded=False):
        self.periodicity = periodicity
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.tasking = False
        self.threaded=threaded
        self._thread = None


    def init(self):
        with psycopg2.connect(dbname=self.dbname,host=self.host,password = self.password,port=self.port,user=self.user) as conn:
            cursor = conn.cursor()
            cursor.execute('''create table if not exists task
                (
                    id          serial,
                    status      integer not null default 0,      -- 0 - новая, 1 - в работе, 2 - выполнена
                    adress      text,
                    theme       text,
                    message    text
                );

                create index if not exists task__status__idx on task (status);''')
    
    
    def createTask(self,data):
        with psycopg2.connect(dbname=self.dbname,host=self.host,password = self.password,port=self.port,user=self.user) as conn:
            cursor = conn.cursor()
            cursor.execute("insert into task (status,adress,theme,message) values (0,'{}','{}','{}') on conflict do nothing".format(*data.split('/')))
    
    def start(self,sourse):
        self.tasking = True
        def tasking():
            for data in sourse:
                if self.tasking:
                    self.createTask(data)
                    time.sleep(self.periodicity)
                else:
                    break
        
        if self.threaded:
            self._thread = threading.Thread(target=tasking,daemon=True)
            self._thread.start()
            print('Startanuli')
        else:
            try:
                while True:
                    tasking()
            except KeyboardInterrupt:
                pass

    def stop(self):
        self.tasking = False

class worker():
    def __init__(self,dbname,user,password,host,port,periodicity_start=5,periodicity_end=10):
        self.periodicity_start = periodicity_start
        self.periodicity_end = periodicity_end
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.activeListen = True

        self._logger = logging.getLogger("Worker")
        self._logger.setLevel(logging.INFO)
        fh = logging.FileHandler("mail_logs.log",encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        fh.setFormatter(formatter)
        self._logger.addHandler(fh)
        self._logger.info("Program started")

    def listen(self):
        with psycopg2.connect(dbname=self.dbname,host=self.host,password = self.password,port=self.port,user=self.user) as conn:
            cursor = conn.cursor()
            try:
                while self.activeListen:
                    cursor.execute('''with next_task as (
                                        select id,task.adress,task.theme,task.message from task
                                        where status = 0
                                        limit 1
                                        for update skip locked
                                    )
                                    update task
                                    set
                                        status = 1
                                    from next_task
                                    where task.id = next_task.id
                                    returning task.id,task.adress,task.theme,task.message; ''')
                    conn.commit()
                    self.execute(cursor.fetchall())
                    time.sleep(4)
            except KeyboardInterrupt:
                self._logger.info('Closing...')
                

    def execute(self,task):
        if task:
            task = task[0]
            self._logger.info('Send {}:{} to {};'.format(task[2],task[1],task[3]))
            with psycopg2.connect(dbname=self.dbname,host=self.host,password = self.password,port=self.port,user=self.user) as conn:
                cursor = conn.cursor()
                cursor.execute('''update task
                                    set
                                        status = 2
                                    where task.id = {} '''.format(task[0]))

        else:
            time.sleep(5)

if __name__ == '__main__':
    tasks = tasker(dbname='TaskDB',host='localhost',password = 'passwd',port='5433',user='postgres')
    tasks.init()
    name = worker(dbname='TaskDB',host='localhost',password = 'passwd',port='5433',user='postgres')
    name.listen()