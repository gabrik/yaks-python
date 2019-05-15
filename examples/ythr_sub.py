import time
import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value
import threading
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-y", "--yaks", required=True,
                help="ip:port for the Yaks service")

ap.add_argument("-z", "--zenoh", required=False,
                help="ip:port for the zenoh service")

args = vars(ap.parse_args())
ylocator = args['yaks']
zlocator = args.get('zenoh')
print('Zenoh locator: {}'.format(zlocator))

y = Yaks.login(ylocator, zlocator)
ws = y.workspace('/')
N = 20000
count = 0
start = 0


def listener(kvs):
    global count
    global start
    global N
    if count == 0:
        start = time.time()
        count += 1
    elif count < N:
        count += 1
    else:
        delta = time.time() - start
        count = 0
        thr = N / delta
        print("{} mgs/sec".format(thr))


path = '/ylatp/sample'
ws.z_subscribe(path, listener)

time.sleep(60)
