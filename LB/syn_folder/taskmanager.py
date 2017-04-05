# -*- coding: UTF-8 -*-.
import Queue
import random
from multiprocessing.managers import BaseManager

# 发送任务的队列
task_queue = Queue.Queue()
# 接受结果的队列
result_queue = Queue.Queue()


# 继承自BaseManager的QueueManager
class QueueManager(BaseManager):
    pass


QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000， 验证码‘abc'：
manager = QueueManager(address=('', 5000), authkey='abc')
# 启动Queue：
manager.start()
# 获得通过网络访问的Queue对象
task = manager.get_task_queue()
result = manager.get_result_queue()
# 放几个任务进去
for i in range(10):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)
# 从result队列读取结果：
print('Try get results...')
for i in range(10):
    r = result.get(timeout=10)
    print('Result: %s' % r)

manager.shutdown()
