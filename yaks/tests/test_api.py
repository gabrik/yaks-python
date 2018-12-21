# Copyright (c) 2018 ADLINK Technology Inc.
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
#
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - Tests

import unittest
import json
from yaks import mvar
from yaks import YAKS

from yaks import Selector
from yaks import Path
from yaks import Value
from yaks.exceptions import *
import time


class APITest(unittest.TestCase):

    def test_create_close_api(self):
        #y = YAKS()
        #self.assertFalse(y.is_connected)
        y = YAKS.login(server_address='127.0.0.1')
        self.assertTrue(y.is_connected)
        y.logout()
        self.assertFalse(y.is_connected)

    def test_create_delete_storage(self):
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        sid = y.create_storage('123', properties)
        self.assertEqual(sid, '123')
        y.remove_storage(sid)
        y.logout()

    def test_create_delete_storage_non_str_id(self):
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        sid = y.create_storage(123, properties)
        self.assertEqual(sid, '123')
        y.remove_storage(sid)
        y.logout()

    def test_create_delete_workspace(self):
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        sid = y.create_storage('123', properties)
        workspace = y.workspace(Path('/myyaks'))
        self.assertEqual(sid, '123')
        self.assertEqual(workspace.path, Path('/myyaks'))
        workspace.dispose()
        y.remove_storage(sid)
        y.logout()

    def test_put_get_remove(self):
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        sid = y.create_storage('123', properties)
        workspace = y.workspace(Path('/myyaks'))
        d = Value(json.dumps({'value': 1}))
        self.assertTrue(workspace.put(Path('/myyaks/key1'), d))
        nd = workspace.get(Selector('/myyaks/key1'), paths_as_strings=False)[0]
        k = nd.get('key')
        v = nd.get('value')
        self.assertEqual(v, d)
        self.assertEqual(k, Path('/myyaks/key1'))
        d = Value(json.dumps({'value': 2}))
        self.assertTrue(workspace.remove(Path('/myyaks/key1')))
        self.assertEqual(workspace.get(Selector('/myyaks/key1'),
                                       paths_as_strings=False), [])
        workspace.dispose()
        y.remove_storage(sid)
        y.logout()

    def test_put_get_remove_strings(self):
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': '/myyaks'}
        sid = y.create_storage('123', properties)
        workspace = y.workspace('/myyaks')
        d = Value(json.dumps({'value': 1}))
        self.assertTrue(workspace.put('/myyaks/key1', d))
        nd = workspace.get('/myyaks/key1')[0]
        k = nd.get('key')
        v = nd.get('value')
        self.assertEqual(v, d)
        self.assertEqual(k, '/myyaks/key1')
        d = Value(json.dumps({'value': 2}))
        self.assertTrue(workspace.remove('/myyaks/key1'))
        self.assertEqual(workspace.get('/myyaks/key1'), [])
        workspace.dispose()
        y.remove_storage(sid)
        y.logout()

    def test_sub_unsub(self):
        #self.assertTrue(True)
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        stid = y.create_storage('123', properties)
        workspace = y.workspace(Path('/myyaks'))
        local_var = mvar.MVar()

        def cb(kvs):
            self.assertEqual(kvs,
                             [{'key': Path('/myyaks/key1'),
                               'value': Value('123')}])
            local_var.put(kvs)

        sid = workspace.subscribe(
            Selector('/myyaks/key1'), cb, paths_as_strings=False)
        workspace.put(Path('/myyaks/key1'), Value('123'))
        self.assertEqual(local_var.get(),
                         [{'key': Path('/myyaks/key1'),
                              'value': Value('123')}])
        self.assertTrue(workspace.unsubscribe(sid))
        workspace.dispose()
        y.remove_storage(stid)
        y.logout()

    def test_eval(self):
        #self.assertTrue(True)
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        stid = y.create_storage('123', properties)
        workspace = y.workspace(Path('/myyaks'))

        def cb(path, hello):
            return Value('{} World!'.format(hello))

        workspace.eval(Path('/myyaks/key1'), cb, paths_as_strings=False)
        kvs = workspace.get(
            Selector('/myyaks/key1?[hello=mondo]'), paths_as_strings=False)
        self.assertEqual(kvs,
                         [{'key': Path('/myyaks/key1'),
                              'value': Value('mondo World!')}])
        workspace.remove(Path('/myyaks/key1'))
        workspace.dispose()
        y.remove_storage(stid)
        y.logout()

    def test_sub_unsub_strings(self):
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        stid = y.create_storage('123', properties)
        workspace = y.workspace(Path('/myyaks'))
        local_var = mvar.MVar()

        def cb(kvs):
            self.assertEqual(kvs,
                             [{'key': '/myyaks/key1',
                               'value': Value('123')}])
            local_var.put(kvs)
        sid = workspace.subscribe('/myyaks/key1', cb)
        workspace.put('/myyaks/key1', Value('123'))
        self.assertEqual(local_var.get(),
                         [{'key': '/myyaks/key1',
                            'value': Value('123')}])
        self.assertTrue(workspace.unsubscribe(sid))
        workspace.dispose()
        y.remove_storage(stid)
        y.logout()

    def test_eval_string(self):
        #self.assertTrue(True)
        y = YAKS.login(server_address='127.0.0.1')
        properties = {'is.yaks.storage.selector': Selector('/myyaks')}
        stid = y.create_storage('123', properties)
        workspace = y.workspace(Path('/myyaks'))

        def cb(path, hello):
            self.assertTrue(isinstance(path, str))
            return Value('{} World!'.format(hello))

        workspace.eval('/myyaks/key1', cb)
        kvs = workspace.get('/myyaks/key1?[hello=mondo]')
        self.assertEqual(kvs,
                         [{'key': '/myyaks/key1',
                              'value': Value('mondo World!')}])
        workspace.remove('/myyaks/key1')
        workspace.dispose()
        y.remove_storage(stid)
        y.logout()
