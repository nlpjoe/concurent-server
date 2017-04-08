from twisted.internet import reactor
from twisted.enterprise import adbapi
import psycopg2


def getSites():
    return dbpool.runQuery("select * from TypeTable")


def printResult(l):
    for item in l:
        print item


dbpool = adbapi.ConnectionPool(
    'psycopg2', user="joe", password="zjz666",
    host="192.168.10.50", database="collectiondb")
getSites().addCallback(printResult)
reactor.callLater(4, reactor.stop)
reactor.run()
