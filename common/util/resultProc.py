#!/usr/bin/env python
import MySQLdb
import os,sys, traceback
import logging, config
from patterns import Singleton 

class logManager:
	class log:
		def __init__(self,logfile,  logLevel = logging.DEBUG, logformatter = '%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s'):
			self.logger = logging.getLogger(logfile)
			self.hdlr = logging.FileHandler(logfile)
			self.stream_hdlr = logging.StreamHandler(sys.stdout)
			formatter = logging.Formatter(logformatter)
			self.hdlr.setFormatter(formatter)
			self.stream_hdlr.setFormatter(formatter)
			self.logger.addHandler(self.hdlr)
			self.logger.addHandler(self.stream_hdlr)
			self.logger.setLevel(logLevel)
		def __del__(self):
			self.logger.removeHandler(self.hdlr)
		def getLogger(self):
			return self.logger
	
	class traceLog():
		def __init__(self):
			Singleton.__init__(self)
			self.hdlr = logManager.log(os.path.normpath('resultProc.log'))
		def __call__(self):
			return self.hdlr.getLogger()
		

class db_op_failure(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
            
class resultProc:
	def __init__(self, logfile, *exeInfo):
		self.logFile = logfile
		self.exeInfo = exeInfo
		#self.conn = MySQLdb.connect(host=config.parameters.get('db_host'),user=config.parameters.get('db_user'),passwd=config.parameters.get('db_passwd'),db=config.parameters.get('database'))
		self.conn = MySQLdb.connect(host='localhost',user='root', passwd='root000',db='auto_sharable_db')
		self.cursor = self.conn.cursor()
		self.tracelLog = logManager.traceLog()()
	
	def __del__(self):
		self.cursor.close()
		self.conn.close()	
	
	def __commit(self):
		self.conn.commit()
	
	def	__rollback(self):
		self.conn.rollback()
	
	def __getRecs(self):	
		f=open(self.logFile, 'r')
		self.recs = []
		for  i in f:
			rec=i.strip().split('|')
			rec.append(self.exe_id)
			self.recs.append(rec)
		f.close()

	def __insertRec(self):
		self.tracelLog.info('Insert Record info into DB')
		sql = "insert into Record(Feature,Case_Name,Result,Exe_Time,Execution_ID) values(%s,%s,%s,%s,%s)"
		self.__getRecs()
		self.tracelLog.debug(str(self.recs))
		if self.cursor.executemany(sql,self.recs) != len(self.recs):
			raise db_op_failure('Insert Record fail!')
		self.recs=None	

	def __insertExe(self):
		self.tracelLog.info('Insert execution info into DB')
		self.tracelLog.info(str(self.exeInfo))
		
		sql = "insert into Execution(Start_Time,End_Time,Suite_ID,Version) values(%s,%s,%s,%s)"
		if self.cursor.execute(sql,self.exeInfo) != 1:
			raise db_op_failure('Insert Execution fail!')
		sql='select id from Execution where Start_Time=%s and End_time=%s and Suite_ID = %s and Version = %s'
		
		if self.cursor.execute(sql, self.exeInfo) < 1:
			raise db_op_failure('select Execution fail!')
		recs = self.cursor.fetchall()
		self.exe_id = recs[0][0]
		self.tracelLog.debug('Execution record: ' + str(recs))	
	
	def __insertStatistic(self):
		self.tracelLog.debug("Insert statistic into DB")
		sql = '''select Feature, lower(Result) Result, count(*) num from Record where Execution_ID=%s group by Feature, lower(Result)''' 
		if self.cursor.execute(sql,(self.exe_id,)) < 1:
			raise db_op_failure('Select Execution fail(for statistic)!')
		recs = self.cursor.fetchall()
		self.tracelLog.debug("Rcords info: " + str(recs))
		stat_info={}
		for i in recs:
			stat_info[i[0]] = stat_info.get(i[0],{'pass':0, 'fail':0, 'error':0, 'none':0})
			stat_info[i[0]][i[1]] = i[2]
		recs=[]	
		self.tracelLog.debug("stat info: " + str(stat_info))
		for i in stat_info:
			recs.append((i,stat_info[i]['pass'],stat_info[i]['fail'],stat_info[i]['error'],stat_info[i]['none'], self.exe_id))
		self.tracelLog.debug("statistic info: " + str(recs))			
		sql = "insert into Statistic(Feature,Pass,Fail,Error,None,Execution_ID) values(%s,%s,%s,%s,%s,%s)"
		if self.cursor.executemany(sql,recs) != len(recs):
			raise db_op_failure('Insert statistic fail!')
			
	def run(self):
		self.tracelLog.info('Start to import test result into DB')
		try:
			self.__insertExe()
			self.__insertRec()
			self.__insertStatistic()
		except Exception as e:
			self.__rollback()
			traceback.print_exc()
			self.tracelLog.error(str(e))
			raise e
		self.__commit()
		self.tracelLog.info('Finished to import test result into DB')
		return self.exe_id