# -*- coding: UTF-8 -*-.
__author__ = 'Joe'

from nose.tools import with_setup
from nose.tools import assert_equal

import time
from finaldesign.client.datasimulator import DataSimulator


def setUp():
    print("============test Client module setup   ==============")


def teardown():
    print("\n============test Client module teardown==============")


def test_data_simulator():
    print("============test data simulator ==============")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    result1 = DataSimulator().get_data(1)
    print result1
    assert 0 <= result1[0] <= 250
    assert_equal(result1[1], timestamp)
