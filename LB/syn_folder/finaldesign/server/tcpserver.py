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
        print postStr
        d = self.dbpool.runOperation(postStr)
        return d

    def printResult(self, l):
        if not l:
            return
        for item in l:
            # print item
            pass

    def handle_request(self, line):
        data = line.split(',')
        self.postData(data).addCallback(self.printResult)

    def lineReceived(self, line):
        d = deferToThread(self.handle_request, line)
        d.addCallbacks(self.factory.cbSucceed, self.factory.cbFailed)

    def connectionMade(self):
        print 'connectionMade.'
        self.dbpool = adbapi.ConnectionPool(
            'psycopg2', user="joe",
            password="zjz666", host="192.168.10.50",
            database="collectiondb")

    def connectionLost(self, reason):
        print 'connectionLost'
        for item in self.factory.errors:
            print item


class ServerProtocolFactory(protocol.Factory):
    """docstring for ServerProtocolFactory"""
    protocol = ServerProtocol

    def __init__(self):
        self.failcnt = 0
        self.successcnt = 0
        self.successes = []
        self.errors = []

    def buildProtocol(self, addr):
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
