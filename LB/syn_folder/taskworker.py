# -*- coding: UTF-8 -*-.
import Queue
import time
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


# 由于这里的QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')


server_addr = '192.168.10.101'
m = QueueManager(address=(server_addr, 5000), authkey='abc')
m.connect()
print 'Connected to server %s...' % server_addr
# 获取Queue的对象
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列中取任务，并把结果写入result队列：
while True:
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        # time.sleep(0.5)
        result.put(r)
    except Queue.Empty:
        print 'task queue is empty.'

print 'worker exit.'
