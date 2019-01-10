from yaks import Yaks
from yaks import Selector
from yaks import Path
from yaks import Value
from yaks import Encoding
import sys
import json


def obs(kvs):
    print('Called OBSERVER KVS: {}'.format(kvs))


def evcb(path, param):
    print('Executing eval on {}'.format(path))
    return Value('executed {}'.format(param))


def main():
    print('creating api')
    y = Yaks.login(sys.argv[1])

    print('>> Create workspace and subscription')
    input()
    workspace = y.workspace('/myyaks')

    sid = workspace.subscribe('/myyaks/example/**', obs)

    print('>> Put Tuple')
    input()
    workspace.put('/myyaks/example/one',
                  Value('hello!', encoding=Encoding.STRING))

    print('>> Put Tuple')
    input()
    workspace.put('/myyaks/example/two', Value('hello2!'))

    print('>> Put Tuple')
    input()
    workspace.put('/myyaks/example/three', Value('hello3!'))

    print('>> Put Tuple JSON as RAW')
    input()
    d = Value({'this': 'is', 'a': 'json'}, encoding=Encoding.JSON)
    workspace.put('/myyaks/example/four', d)

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get('/myyaks/example/one')))

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get('/myyaks/example')))

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get('/myyaks/example/*')))

    print('>> Remove Tuple')
    input()
    print('REMOVE: {}'.format(workspace.remove('/myyaks/example/one')))

    print('>> Get Removed Tuple')
    input()
    print('GET: {}'.format(workspace.get('/myyaks/example/one')))

    print('>> Unsubscribe')
    input()
    if sid:
        workspace.unsubscribe(sid)

    print('>> Put Tuple')
    input()
    workspace.put('/myyaks/example2/three',
                  Value('hello3!', encoding=Encoding.STRING))

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get('/myyaks/example/three')))

    print('>> Create subscription without listener')
    input()
    sid2 = workspace.subscribe('/myyaks/example2/**')

    print('>> Put Tuple')
    input()
    workspace.put('/myyaks/example2/three',
                  Value('hello3!', encoding=Encoding.STRING))

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get('/myyaks/example2/three')))

    print('>> Unsubscribe')
    input()
    if sid2:
        workspace.unsubscribe(sid2)

    print('>> Register Eval')
    input()
    workspace.register_eval('/myyaks/key1', evcb)

    print('>> Get on Eval')
    input()
    print('GET: {}'.format(workspace.eval('/myyaks/key1?[param=1]')))

    print('>> Unregister Eval')
    input()
    workspace.unregister_eval('/myyaks/key1')

    print('>> Dispose Access')
    input()

    #workspace.dispose()

    # print('>> Dispose Storage')
    # input()
    # y.remove_storage(myst_id)
    print('>> Close')
    input()
    y.logout()
    print('bye!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[Usage] {} <yaks server address>'.format(sys.argv[0]))
        exit(-1)
    main()
