# -*- coding: UTF-8 -*-.
'''
用于实现给响应客户端的请求，并且可以给客户发送消息，
'''

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
import time
import thread

#线程体，
def timer(no, interval):
    while True:
        time.sleep(interval)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        for element in MyFactory.clients:
            print(element) #在这里可以给每个客户端发送消息
            element.transport.getHandle().sendall('dddddddddddd')
    thread.exit_thread()


class MyProtocal(Protocol):
    def __init__(self):
        print("43:MyProtocal __init__")
        pass
        
    def connectionMade(self):
        print("24:MyProtocal connectionMade")
        self.factory.addClient(self)
        # thread.start_new_thread(timer, (1, 3))

    def connectionLost(self, reason):
        print("MyProtocal connectionLost")
        #print(reason)
        self.factory.deleteClient(self)

    def dataReceived(self, data):
        print("MyProtocal dataReceived")
        self.transport.write('okthis is ok ') #在这里接收用户的请求认证，并返回数据，发送数据请使用transport.getHandle().sendall() 保证数据立刻发送到客户端

class MyFactory(Factory):

    protocol = MyProtocal
    clients=[] #用户保存客户端列表，

    def __init__(self):
        print("43:MyFactory __init__")
        pass
        #启动线程用于处理用于给客户端主动发送数据

    def addClient(self, newclient):
        print("MyFactory addClient")
        print(newclient)
        self.clients.append(newclient)

    def deleteClient(self, client):
        print("MyFactory deleteClient")
        print(client)
        self.clients.remove(client)

reactor.listenTCP(9999, MyFactory())
reactor.run()