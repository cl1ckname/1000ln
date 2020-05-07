"""Create queue of tasks with PostrgeSQL and execute it.

Classes:

    Pickler
    Unpickler

"""

import psycopg2
import time
import logging
import threading

class Tasker():
    """ Class to create a queqe of tasks with text document."""

    def __init__(self, dbname, user, password, host, port, 
                            periodicity=3, threaded=False):
        self.periodicity = periodicity
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.tasking = False
        self.threaded = threaded
        self._thread = None


    def init(self):
        """Initialization the database to storage the tasks."""

        with psycopg2.connect(dbname=self.dbname,host=self.host, password = self.password,port=self.port, user=self.user) as conn:
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
        """ Create task from string """
        with psycopg2.connect(dbname=self.dbname,host=self.host,password = self.password,port=self.port,user=self.user) as conn:
            cursor = conn.cursor()
            cursor.execute("insert into task (status,adress,theme,message) values (0,'{}','{}','{}') on conflict do nothing".format(*data.split('/')))

    def start(self,sourse):
        """ Start to create tasks automaticlly """
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
        else:
            try:
                while True:
                    tasking()
            except KeyboardInterrupt:
                pass

    def stop(self):

        """ Stop to create tasks automaticlly """

        self.tasking = False

class Worker():
    """ Class to listen database and execute tasks """
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

    def listen(self,threaded=False):
        """ Functon to read database and creating of tasks queue. """
        self.activeListen = True
        def check():
            with psycopg2.connect(dbname=self.dbname,host=self.host,password = self.password,port=self.port,user=self.user) as conn:
                cursor = conn.cursor()
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

        if threaded:
            threading.Thread(target=check,daemon=True).start()
        else:
            try:
                check()
            except KeyboardInterrupt:
                self._logger.info('Stoping...')

    def stop(self):
        """ Stop reading database """

        self.activeListen = False

    def execute(self,task):
        """Function to execute tasks."""

        if task:
            task = task[0]
            self._logger.info('Send {}:{} to {}'.format(task[2],task[1],task[3]))
            with psycopg2.connect(dbname=self.dbname, host=self.host, password = self.password, port=self.port, user=self.user) as conn:
                cursor = conn.cursor()
                cursor.execute('''update task
                                    set
                                        status = 2
                                    where task.id = {} '''.format(task[0]))

        else:
            time.sleep(5)