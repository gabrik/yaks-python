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
import mvar
import time
from yaks import Yaks
from papero import Property
from yaks import Selector
from yaks import Path
from yaks import Value
from yaks.exceptions import ValidationError
from yaks import Encoding


class APITest(unittest.TestCase):

    def test_create_close_api(self):
        y = Yaks.login('127.0.0.1')
        self.assertTrue(y.rt.running)
        y.logout()
        self.assertFalse(y.rt.running)

    def test_create_delete_storage(self):
        y = Yaks.login('127.0.0.1')
        admin = y.admin()
        properties = [Property('selector', '/myyaks/**')]
        stid = '123'
        res1 = admin.add_storage(stid, properties)
        res2 = admin.remove_storage(stid)
        y.logout()
        self.assertTrue(res1)
        self.assertTrue(res2)

    def test_create_delete_workspace(self):
        y = Yaks.login('127.0.0.1')
        admin = y.admin()
        properties = [Property('selector', '/myyaks/**')]
        stid = '123'
        admin.add_storage(stid, properties)
        workspace = y.workspace('/myyaks')
        self.assertEqual(workspace.path, Path('/myyaks'))
        admin.remove_storage(stid)
        y.logout()

    def test_put_get_remove(self):
        y = Yaks.login('127.0.0.1')
        admin = y.admin()
        properties = [Property('selector', '/myyaks/**')]
        stid = '123'
        admin.add_storage(stid, properties)
        workspace = y.workspace('/myyaks')
        d = Value('hello!', encoding=Encoding.STRING)
        self.assertTrue(workspace.put('/myyaks/key1', d))
        nd = workspace.get('/myyaks/key1')[0]
        k, v = nd
        self.assertEqual(v, d)
        self.assertEqual(k, '/myyaks/key1')
        self.assertTrue(workspace.remove('/myyaks/key1'))
        self.assertEqual(workspace.get('/myyaks/key1'), [])
        admin.remove_storage(stid)
        y.logout()

    def test_sub_unsub(self):
        y = Yaks.login('127.0.0.1')
        admin = y.admin()
        properties = [Property('selector', '/myyaks/**')]
        stid = '123'
        admin.add_storage(stid, properties)
        workspace = y.workspace('/myyaks')
        local_var = mvar.MVar()

        def cb(kvs):
            self.assertEqual(kvs,
                             [('/myyaks/key1',
                               Value('123', encoding=Encoding.STRING))])
            local_var.put(kvs)

        sid = workspace.subscribe('/myyaks/key1', cb)
        workspace.put('/myyaks/key1', Value('123', encoding=Encoding.STRING))
        self.assertEqual(local_var.get(),
                         [('/myyaks/key1',
                           Value('123', encoding=Encoding.STRING))])
        self.assertTrue(workspace.unsubscribe(sid))
        admin.remove_storage(stid)
        y.logout()

    def test_eval(self):
        y = Yaks.login('127.0.0.1')
        admin = y.admin()
        properties = [Property('selector', '/myyaks/**')]
        stid = '123'
        admin.add_storage(stid, properties)
        workspace = y.workspace('/myyaks')

        def cb(path, hello):
            return Value('{} World!'.format(hello), encoding=Encoding.STRING)

        workspace.register_eval('/myyaks/key1', cb)
        kvs = workspace.eval('/myyaks/key1?(hello=mondo)')
        self.assertEqual(kvs,
                         [('/myyaks/key1',
                           Value('mondo World!', encoding=Encoding.STRING))])
        workspace.unregister_eval('/myyaks/key1')
        admin.remove_storage(stid)
        y.logout()
