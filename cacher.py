#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import time


class Cache(object):
    def __init__(self, max_age=3600):
        self.max_age = max_age
        self.storage = {}

    def add(self, key, data):
        ts = time.time()
        self.storage[key] = (ts, data)

    def get(self, key):
        ts = time.time()
        if key not in self.storage:
            return None

        if ts - self.storage[key][0] > self.max_age:
            return None

        return self.storage[key][1]


def main():
    pass

if __name__ == '__main__':
    main()
