# -*- coding: UTF-8 -*-.
# 前端客户端模拟

import time, random


class DataSimulator(object):
    """模拟数据产生器
1. PM2.5        数值范围[0, 250]
2. Humidity     数值范围[0, 100]
3. Temperature  数值范围[-40, 50]
4. VehicleSpeed 数值范围[0, 200]
    """
    def __init__(self):
        pass

    def get_data(self, type):
        switcher = {
            1: random.randint(0, 250),
            2: round(random.uniform(0, 100), 2),
            3: round(random.uniform(-40, 50), 2),
            4: round(random.uniform(0, 200), 2)
        }
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return (switcher.get(type, "unknown-type"), timestamp)
