#!/usr/bin/env python
import MySQLdb
import os,sys
import logManager

class db_op_failure(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

task=None
input_path=None
def get_task(result_path):
    global task
    global input_path
    if input_path is None:
        input_path=result_path
    if task is None:
        f = open(os.path.join(os.path.normpath(result_path),'task.log'), "r")
        try:
            task=f.readline().rstrip()
            task = task.split('|')
        except:
            raise
        finally:
            f.close()
    job=task[-1]
    task[-1]=input_path+'/result.'+task[3].replace(' ','_')
    task.append(job)
    return task

def upload_task(result_path):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='root000',db='XIV_TEST')
        cursor = conn.cursor()
        task=get_task(result_path)
        sql = "insert into TEST_TASKS(XIV_VERSION,CODE_VERSION,GIT_HEAD,EXE_DATETIME,EXE_MACHINE,TARGET_MACHINE,result,job) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        if cursor.execute(sql,task) != 1:
            raise db_op_failure('Insert TEST_TASKS fail!')
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def upload_result(result_path):
    task=get_task(result_path)
    if 'GEN3' == task[0].upper():
        rec_t = 'GEN3_TC_RECORDS'
    else:
        rec_t = 'GEN2_TC_RECORDS'
    f = open(os.path.join(os.path.normpath(result_path),'result.log'), "r")
    f_std = open(os.path.join(os.path.normpath(result_path),'std_tcs.log'), "r")
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='root000',db='XIV_TEST',charset="utf8")
        cursor = conn.cursor()
        sql='select id from TEST_TASKS where XIV_VERSION=%s and CODE_VERSION=%s and EXE_DATETIME=%s'
        param = (task[0], task[1], task[3])
        print param
        if cursor.execute(sql, param) < 1:
            raise db_op_failure('select TEST_TASKS fail!')
        recs = cursor.fetchall()

        sql = 'insert into ' + rec_t + '(MODULE, TC_ID, STATUS, TASK_ID) values(%s, %s, %s, %s)'

        for i in f_std:
            std = i.strip()
            if std == '':
                continue
            rec = std.split('/')
            rec.append('NONE')
            rec.append(str(recs[0][0]))
            if cursor.execute(sql, rec) != 1:
                raise db_op_failure('insert '+ rec_t + ' fail!')
        sql = 'update ' + rec_t + ' set STATUS=%s where TASK_ID=%s and MODULE=%s and TC_ID=%s'
        sql2='select id from ' + rec_t + ' where TASK_ID=%s and MODULE=%s and TC_ID=%s'
        for i in f.readlines():
            rec = i.rstrip().split('/')
            param2 = (str(recs[0][0]), rec[0], rec[1])
            if cursor.execute(sql2, param2) < 1:
                continue
            param = (rec[2], str(recs[0][0]), rec[0], rec[1])
            if cursor.execute(sql, param) != 1:
                raise db_op_failure('update '+ rec_t + ' fail!')

        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        f.close()

def upload(result_path):
    upload_task(result_path)
    upload_result(result_path)

def run(result_path):
    upload(logManager.LogHome)
    t=get_task(logManager.LogHome)
    ret=os.system("mv "+logManager.LogHome+' '+ result_path + os.sep + 'logs_'+ t[-2])
    if ret != 0:
        print "Failure: mv "+logManager.LogHome+' '+ result_path + os.sep + 'logs_'+ t[-2]
        exit(-1)

if __name__ == '__main__':
    if len(sys.argv)<2:
        print "usage: " + sys.argv[0] + " result_path"
        exit(-1)
    input_path=sys.argv[1]
    upload(sys.argv[1]+'/tmp/result')
    t=get_task(sys.argv[1])
    ret=os.system("mv "+sys.argv[1]+'/tmp/result ' + t[-2])
    if ret != 0:
        print "Failure: mv "+sys.argv[1]+'/tmp/result ' + t[-2]
        exit(-1)

