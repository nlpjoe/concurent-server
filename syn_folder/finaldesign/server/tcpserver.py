# -*- coding: UTF-8 -*-.
'''
接收客户端数据，并且保存在远程数据库，
'''

import psycopg2
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.threads import deferToThread
from twisted.enterprise import adbapi


class ServerProtocol(LineReceiver):

    def __init__(self, factory):
        self.factory = factory

    def postData(self, data):
        """
        Post一条数据, 返回一个Deferred
        """
        postStr = "INSERT INTO frontdatatable (IP, typeid, data, datetime)" \
            " VALUES ('%s', %d, '%s', '%s')" % (data[0], int(data[1]), data[2], data[3])
        # print postStr
        d = self.dbpool.runOperation(postStr)
        return d

    def handle_request(self, line):
        data = line.split(',')
        self.postData(data)

    def lineReceived(self, line):
        d = deferToThread(self.handle_request, line)
        d.addCallbacks(self.factory.cbSucceed, self.factory.cbFailed)

    def connectionMade(self):
        print '%d:connectionMade.Connected from %s:%s' % \
        (self.factory.connection_num, self.transport.getPeer().host, self.transport.getPeer().port)
        self.dbpool = adbapi.ConnectionPool(
            'psycopg2', user="joe",
            password="zjz666", host="192.168.10.50",
            database="collectiondb")

    def connectionLost(self, reason):
        self.factory.connection_num -= 1
        print 'Connection closed with %s:%s' % (self.transport.getPeer().host, self.transport.getPeer().port)
        for item in self.factory.errors:
            print item


class ServerProtocolFactory(protocol.Factory):
    """docstring for ServerProtocolFactory"""
    protocol = ServerProtocol

    def __init__(self):
        self.connection_num = 0
        self.failcnt = 0
        self.successcnt = 0
        self.successes = []
        self.errors = []

    def buildProtocol(self, addr):
        self.connection_num += 1
        return ServerProtocol(self)

    def cbSucceed(self, msg):
            self.successcnt += 1
            str = '%d:InsertSucceed' % self.successcnt
            self.successes.append(str)

    def cbFailed(self, msg):
            self.failcnt += 1
            str = '%d:InsertFailed' % self.failcnt
            self.errors.append(str)

reactor.listenTCP(10010, ServerProtocolFactory())
reactor.run()
