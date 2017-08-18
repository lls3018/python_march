#!/usr/bin/python
#coding=utf-8

from Person import Person

class Queue(object):

    def __init__(self):
        self.queue = []

    def __str__(self):
        return str(self.queue)

    # 打印队列
    def showQueue(self):
        show_queue = []
        for ele in self.queue:
            show_queue.append(str(ele))
        print show_queue
        print '----------------'

    #获取队列的当前长度
    def getSize(self):
      return len(self.queue)

    #入队, 将元素插入队列尾
    def enqueue(self, item):
        if isinstance(item, Person):
            if self.isempty():
                self.queue.append(item)
            else:
                positon = len(self.queue)-1
                while positon >=0 and (self.queue[positon]).typevalue < item.typevalue:
                    positon = positon - 1
                self.queue.insert(positon+1, item)
        else:
            raise Exception("Only Person can be enqueue")

    #出队，如果队列空了返回-1或抛出异常，否则返回队列头元素并将其从队列中移除
    def dequeue(self):
        if self.isempty() :
            return -1
        firstElement = self.queue[0]
        self.queue.remove(firstElement)
        return firstElement

    #判断队列空
    def isempty(self):
        if len(self.queue) == 0:
            return True
        return False


if __name__ == '__main__' :
    queueTest = Queue()
    p1 = Person(38, 'Regular')
    p2 = Person(30, 'Pregnant')
    p3 = Person(24, 'Disabled')
    p4 = Person(60, 'Regular')
    p5 = Person(32, 'Pregnant')

    queueTest.enqueue(p1)
    queueTest.enqueue(p2)
    queueTest.enqueue(p3)
    queueTest.enqueue(p4)
    queueTest.enqueue(p5)
    queueTest.showQueue()
    queueTest.enqueue(1)

