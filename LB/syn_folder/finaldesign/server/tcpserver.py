# -*- coding: UTF-8 -*-.
'''
接收客户端数据，并且保存在远程数据库，
'''

from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.threads import deferToThread


class ServerProtocol(LineReceiver):
    """docstring for ServerProtocol"""
    # def dataReceived(self, data):
    #     self.transport.write(data)
    #     print data

    def lineReceived(self, line):
        self.transport.write(line)
        print line


class ServerProtocolFactory(protocol.Factory):
    """docstring for ServerProtocolFactory"""
    protocol = ServerProtocol


reactor.listenTCP(10010, ServerProtocolFactory())
reactor.run()
