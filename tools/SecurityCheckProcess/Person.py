#!/usr/bin/python
#coding=utf-8

class Person(object):

    def __init__(self, age, type):
        self.age = age
        self.type = type

    def __str__(self):
      return str(self.age) + "-"+ self.type

    @property
    def typevalue(self):
        if self.type == 'Pregnant':
            return 3
        if self.type == 'Disabled':
            return 2
        if self.type == 'Regular':
            if self.age >= 60:
                return 1
            return 0