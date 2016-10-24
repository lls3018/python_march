#!/usr/bin/env python
# encoding: utf-8

# test.py
import unittest
from function import add_and_multiply


class MyTestCase(unittest.TestCase):
    def test_add_and_multiply(self):

        x = 3
        y = 5

        addition, multiple = add_and_multiply(x, y)

        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)
