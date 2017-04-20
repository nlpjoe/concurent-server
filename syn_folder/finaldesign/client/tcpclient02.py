# -*- coding: UTF-8 -*-.
# 前端客户端模拟 多进程测试

from multiprocessing import Pool



def main(pro_num):


if __name__ == '__main__':
    p = Pool(4)
    for i in xrange(4):
        p.apply_async(main, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
