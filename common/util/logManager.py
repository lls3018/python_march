#!/usr/bin/python

import logging
import time
import os, sys,types
from os.path import expanduser
import config,postprocess
from patterns import Singleton
import httpclient

para =  config.parameters()
Logformatter = '%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s'
LogLevel = para.get('log_level') #logging.NOTSET
Postprocess = 'postprocess' #para.get('post_process')
#LogHome = para.get('log_path')
LogHome = expanduser("~") + "/logs"


class global_var:
  feature = 'Unknown'
  cutOffLine="-"*70
  
class log:
  Level_list={'DEBUG':logging.DEBUG,'INFO':logging.INFO,'WARNING':logging.WARNING,'ERROR':logging.ERROR,'CRITICAL':logging.CRITICAL}
  def __init__(self,logfile,  logLevel = Level_list[LogLevel], logformatter = Logformatter):
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
    
class caseLog:
  def __call__(self, case):
    fpath=os.path.normpath(LogHome+os.sep+global_var.feature)
    if not os.path.isdir(fpath):
      #os.mkdir(fpath)
       os.makedirs(fpath)
    self.hdlr = log(os.path.normpath(fpath  + os.sep  + case +'.log'))    
    return self.hdlr.getLogger()

class classLog:
  def __init__(self, name):
    fpath=os.path.normpath(LogHome+os.sep+global_var.feature)
    if not os.path.isdir(fpath):
      #os.mkdir(fpath)
        os.makedirs(fpath)
    self.hdlr = log(os.path.normpath(fpath + os.sep + name + '.log'))
  def __call__(self):
    return self.hdlr.getLogger()
              
class traceLog(Singleton):
  def __init__(self):
    Singleton.__init__(self)
    self.hdlr = log(os.path.normpath(LogHome + os.sep + 'trace.log'))
  def __call__(self):
    return self.hdlr.getLogger()

class writeStatus(Singleton):
  """
    the class handles log file and report test result via httpclient

  """
  def __init__(self):
    self.start_time = time.time()
    self.hdlr = open(os.path.normpath(LogHome + os.sep + 'result.log'),'w')

  def __call__(self, tcName, status):
    #msg = tcName + ' ' + '-'*20 + ' ' + status + ' '*4 + time.strftime('%Y-%m-%d.%H:%M:%S') + os.linesep
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = '|'.join([global_var.feature, tcName, status , timestamp]) + os.linesep
    self.hdlr.write(msg)
    self.hdlr.flush()
    target_dir = os.path.normpath(LogHome + os.sep + tcName.split('.')[0])
    self.postProcess(target_dir,status)
    self.start_time = time.time()
    if para.__getattribute__("buildID") is not None:

        print "buildID Set in Global configuration parameters: " + para.__getattribute__("buildID")
        resultHash = {"Oprand":"RESULTREPORT",
                      "feature":global_var.feature,
                      "tcName":tcName,
                      "result":status,
                      "timestamp":timestamp,
                      "executionID":para.__getattribute__("executionID")}
        para.httpclient.post(resultHash)


    
  def postProcess(self, logPath,status):
    self.end_time = time.time()
    posts=[]
    m_postprocess = __import__(Postprocess)
    for name in dir(m_postprocess):
      obj = getattr(m_postprocess,  name)
      if type(obj) == types.ClassType and issubclass(obj, postprocess.PostProcess):
        posts.append(obj)
        
    for post in posts:
      post()(status,logPath,self.start_time, self.end_time)
      

