# -*- coding: UTF-8 -*-.
# 前端客户端模拟 单点测试

import optparse, sys, time
from sensor import Sensor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, defer, task
from multiprocessing import Pool
from twisted.internet.threads import deferToThread


def parse_args():
    usage = """
    """

    parser = optparse.OptionParser(usage)

    help = "The typeid of sensor which can't be empty."
    parser.add_option('--typeid', type='int', help=help)

    help = "The all task number of sensors.Default is 1000."
    parser.add_option('--num-task', type='int', help=help, default=1000)

    help = "The number of seconds between client's requests.Default is 1s."
    parser.add_option('--delay', type='float', help=help, default=1)

    options, addresses = parser.parse_args()

    if not addresses or not options.typeid:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' in addr:
            host, port = addr.split(':', 1)
        else:
            host = 'localhost'
            port = addr

        if not port.isdigit():
            parser.error('Ports must be an integers')

        return host, int(port)

    return options, map(parse_address, addresses)[0]


class SensorProtocol(Protocol):

    response = ''

    def sendMessage(self, task_num):
        def strWrapper(data):
            """ 封装数据(IP地址 传感器类型ID 采集值 采集时间)"""
            str = '%s:%s,%d,%s,%s\r\n' % (self.host, self.port, data[0], data[1], data[2])
            return str

        time.sleep(self.factory.delay)
        valueStr = strWrapper(self.factory.sensor.get_data())
        print task_num, valueStr
        self.transport.write(valueStr)
        # task.deferLater(reactor, delay=self.factory.delay, self.transport.write, valueStr)

    def dataReceived(self, data):
        self.response += data

    def connectionMade(self):
        '''获得一个连接'''
        self.host = self.transport.getHost().host
        self.port = str(self.transport.getHost().port)
        for i in range(1, self.factory.task_cnt + 1):
            self.sendMessage(i)
        print "All tasks have been done..."
        reactor.stop()

    def connectionLost(self, reason):
        '''丢失一个连接'''
        print "=================connectionLost"
        # reactor.stop()


class SensorClientFactory(ClientFactory):

    protocol = SensorProtocol

    def __init__(self, typeid, task_cnt, delay):
        self.sensor = Sensor(typeid)
        self.task_cnt = task_cnt
        self.delay = delay


def main():
    options, address = parse_args()
    factory = SensorClientFactory(options.typeid, options.num_task, options.delay)
    host, port = address
    reactor.connectTCP(host, port, factory)
    reactor.run()


if __name__ == '__main__':
    main()
