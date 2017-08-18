#!/usr/bin/python
#coding=utf-8

import datetime
import random  # 导入随机数模块，是为了模拟生产者与消费者速度不一致的情形
import threading
import time

import myThread
from Person import Person
from Queue import Queue

Person_Type = ['Pregnant', 'Regular', 'Disabled']

def Producer(sc_queue, lock, starttime, consumer_time):
    while True:
        endtime = datetime.datetime.now()
        if (endtime - starttime).seconds > consumer_time:
            print "排队时间到结束：{0}s".format(consumer_time)  # 180s后排队结束
            break
        lock.acquire()
        person = Person(random.randint(0, 100), Person_Type[random.randint(0, 2)])
        sc_queue.enqueue(person)  # 将结果放入消息队列中
        lock.release()
        time.sleep(random.randrange(6))  # 生产者的生产速度，6s内


def Consumer(sc_queue, starttime, consumer_time):
    while True:
        endtime = datetime.datetime.now()
        if (endtime - starttime).seconds > consumer_time:
            print "检查时间到结束：{0}s".format(consumer_time) # 180s后结束检查
            break
        if sc_queue.isempty():
            time.sleep(random.randrange(3))  # 消费者的消费速度，3s内
        else:
            person = sc_queue.dequeue()  # 取用消息队列中存放的结果
            if random.randint(1, 10) == 1:
                print "检查失败: " + str(person)
                sc_queue.enqueue(person)
                sc_queue.showQueue()
            else:
                print "检查通过: " + str(person)
                sc_queue.showQueue()
                time.sleep(random.randrange(3))  # 消费者的消费速度，3s内


def main():

    sc_queue = Queue()  # 实例化一个队列
    for k in range(10): # 初始化队列中10个person
        person = Person(random.randint(0,100), Person_Type[random.randint(0,2)])
        sc_queue.enqueue(person)
    sc_queue.showQueue()

    starttime = datetime.datetime.now() #记录开始时间
    lock = threading.Lock()
    # 排队生产者，安检消费者
    producer1 = myThread.MyThread(Producer, (sc_queue, lock, starttime, 180), 'producer1')
    #producer2 = myThread.MyThread(Producer, (sc_queue, lock, starttime, 180), 'producer1')
    consumer1 = myThread.MyThread(Consumer, (sc_queue, starttime, 180), 'consumer1')
    threads = [producer1, consumer1]

    for i in threads:
        i.start()

    for i in threads:
        i.join()


if __name__ == '__main__':
    main()



