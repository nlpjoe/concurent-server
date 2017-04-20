from twisted.internet import reactor
from twisted.enterprise import adbapi
import MySQLdb


def getSites():
    return dbpool.runQuery("select * from TypeTable")


def printResult(l):
    for item in l:
        print item


dbpool = adbapi.ConnectionPool('MySQLdb', user="root",
    passwd="zjz666", host="192.168.10.50",
    use_unicode=True, charset='utf8', db="front_data_collection")
getSites().addCallback(printResult)
reactor.callLater(4, reactor.stop)
reactor.run()
