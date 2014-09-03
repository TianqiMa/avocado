#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2014
# Author: Ruda Moura <rmoura@redhat.com>

import sys
import os
import unittest

# simple magic for using scripts within a source tree
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basedir = os.path.dirname(basedir)
if os.path.isdir(os.path.join(basedir, 'avocado')):
    sys.path.append(basedir)

from avocado.plugins import plugin


class NullPlugin(plugin.Plugin):
    pass


class FakePlugin(plugin.Plugin):

    """
    Fake plugin
    """
    name = 'fake'
    enabled = True

    def configure(self, parser):
        self.configured = True

    def activate(self, args):
        self.activated = True

    def run(self, args):
        return 42


class PluginsBasicTest(unittest.TestCase):

    def setUp(self):
        self.p = plugin.Plugin()
        self.null = NullPlugin()
        self.fake = FakePlugin()
        self.disabled_fake = FakePlugin(enabled=False)

    def testCreate(self):
        self.assertTrue(self.p)
        self.assertFalse(self.p.enabled)
        self.assertEqual(self.p.name, 'noname')
        self.assertTrue(self.p.description)
        self.assertTrue(self.null.name, 'noname')
        self.assertFalse(self.null.enabled)
        self.assertTrue(self.fake)
        self.assertEqual(self.fake.name, 'fake')
        self.assertTrue(self.fake.enabled)
        self.assertEqual(self.fake.description, 'Fake plugin')
        self.assertFalse(self.disabled_fake.enabled)

    def testConfigure(self):
        self.fake.configure(None)
        self.assertTrue(self.fake.configured, True)

    def testActivate(self):
        self.p.activate(None)
        self.null.activate(None)
        self.fake.activate(None)
        self.assertTrue(self.fake.activated)

    def testRun(self):
        self.assertEqual(self.fake.run(None), 42)

if __name__ == '__main__':
    unittest.main()