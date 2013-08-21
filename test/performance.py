#!/usr/bin/env python
'''
@author Luke Campbell
@file test/performance.py
@description Testing for Performance
'''
from test.test_case import TestCase
import time

class ProfileContext:
    stat_list=None
    def __init__(self):
        self.stat_list=[]

class TimeIt(object):
    def __init__(self, profile_ctxt):
        self.results = profile_ctxt.stat_list
    def __enter__(self):
        self.i = time.time()
    def __exit__(self, type, value, traceback):
        v = time.time() - self.i
        self.results.append(v)

class PerformanceTestCase(TestCase):
    def __repr__(self):
        name = self.id()
        name = name.split('.')
        for i,n in enumerate(name):
            if n == self.__class__.__name__:
                break
        mod = '.'.join(name[:i])
        cls = '.'.join(name[i:])
        method = name[-1]
        name = ':'.join([mod,cls])
        return '%s (%s)' %(method,name)
    __str__ = __repr__

    def shortDescription(self):
        return None

    def setUp(self):
        self.profile_context = ProfileContext()

    def profile(self, func, *args, **kwargs):
        with TimeIt(self.profile_context):
            func(*args, **kwargs)




