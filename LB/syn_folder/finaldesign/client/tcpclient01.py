# -*- coding: UTF-8 -*-.
# 前端客户端模拟 单点测试

import optparse, sys, time
from sensor import Sensor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, defer
from multiprocessing import Pool
from twisted.internet.threads import deferToThread


def parse_args():
    usage = """
    """

    parser = optparse.OptionParser(usage)

    help = "The all task number of sensors.Default is 1000."
    parser.add_option('--num-task', type='int', help=help, default=1000)

    help = "The number of seconds between client's requests.Default is 0.5s."
    parser.add_option('--delay', type='float', help=help, default=.5)

    options, addresses = parser.parse_args()

    if not addresses:
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
            str = '%s:%s %d %s %s\r\n' % (self.host, self.port, data[0], data[1], data[2])
            return str

        time.sleep(self.factory.delay)
        for sensor in self.factory.sensors:
            valueStr = strWrapper(sensor.get_data())
            print task_num, valueStr
            self.transport.write(valueStr)

    def dataReceived(self, data):
        self.response += data

    def connectionMade(self):
        '''获得一个连接'''
        self.host = self.transport.getHost().host
        self.port = str(self.transport.getHost().port)
        for i in xrange(self.factory.task_cnt):
            self.sendMessage(i)
        print "All tasks have been done..."

    def connectionLost(self, reason):
        '''丢失一个连接'''
        print "=================connectionLost"
        # reactor.stop()


class SensorClientFactory(ClientFactory):

    protocol = SensorProtocol
    sensors = []    # 前端传感器

    def __init__(self, task_cnt, delay):
        self.task_cnt = task_cnt
        self.delay = delay
        self.succeed_num = 0
        self.failed_num = 0
        for i in range(1, 5):
            sensor = Sensor(i)
            self.sensors.append(sensor)

    def finishedOnce(self, msg='200'):    # 完成一次传输
        # print msg
        self.succeed_num += 1

    def failedOnce(self, reason='404'):
        print reason
        self.failed_num += 1

    def taskAllDone(self, msg):
        flen = self.succeed_num + self.failed_num
        print 'flen=%d' % flen
        if flen == self.task_cnt:
            print "All tasks have been done..."
            reactor.stop()


def main():
    options, address = parse_args()
    factory = SensorClientFactory(options.num_task, options.delay)
    host, port = address
    reactor.connectTCP(host, port, factory)
    reactor.run()


if __name__ == '__main__':
    main()
