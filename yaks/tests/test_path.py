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
from yaks import path


class PathTests(unittest.TestCase):

    def test_path_check_ok(self):
        self.assertTrue(path.check('/this/is/a/path'))

    def test_path_check_absolute_ok(self):
        self.assertTrue(path.is_absolute('/this/is/a/absoliute/path'))

    def test_path_check_absolute_ko(self):
        self.assertFalse(path.is_absolute('this/is/a/relative/path'))

    def test_path_prefix(self):
        p = '/this/is/a/path/with/a/prefix'
        self.assertEqual(path.is_prefix(p, '/this/is/a/path'), True)
        self.assertEqual(path.is_prefix(p, '/that/is/a/path'), False)

    def test_path_check_ko_1(self):
        self.assertFalse(path.check('//this/is/a/not/path'))

    def test_path_check_ko_2(self):
        self.assertFalse(path.check('//this/is/a/not/path/**'))

    def test_path_check_ko_3(self):
        self.assertFalse(path.check('//this/is/a/not/path?with=query'))

    def test_path_check_ko_4(self):
        self.assertFalse(path.check('//this/is/a/not/path#fragment'))

    def test_selector_check_ok(self):
        self.assertTrue(path.is_valid_selector('/this/is/a/*/selector'))

    def test_selector_check_ok_2(self):
        self.assertTrue(path.is_valid_selector('this/is/a/*/selector'))

    def test_selector_check_ko(self):
        self.assertFalse(path.is_valid_selector('//this/is/not/a/*/selector'))

    def test_path_query(self):
        p = '/this/is/a/path?with=query&data=somedata'
        q = {'with': 'query', 'data': 'somedata'}
        self.assertEqual(q, path.get_query(p))

    def test_path_query_complex(self):
        p = '/this/is/a/path?with=query&data.level2=somedata'
        q = {'with': 'query', 'data': {'level2': 'somedata'}}
        self.assertEqual(q, path.get_query(p))
