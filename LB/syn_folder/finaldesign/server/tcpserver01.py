from twisted.internet.protocol import Protocol, Factory


class DataHandler(Protocol):

    def connectionMade(self):
        self.factory.numPros += 1
        if self.factory.numPros > 100:
            self.transport.write("Too many connections, try later...")
            self.transport.loseConnection()

    def connectionLost(self):
        self.factory.numPros -= 1

    def dataReceived(self, data):
        self.transport.write(data)


factory = Factory()
factory.protocol = Answer

from twisted.internet import reactor
reactor.listenTCP(8007, factory, interface='192.168.10.102')
reactor.run()
