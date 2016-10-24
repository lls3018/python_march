#!/usr/bin/env python

import os, re, time, sys, traceback
import xivtest, logManager, config, infoCollect
import poster
import random


class run_tcs:
    def __init__(self, buildID=None, executor="master"):
        ##option is non-empty

        print "Initiate test runner, buildID: " + buildID + ", executor: " + executor
        self.buildID = buildID
        self.executor = executor
        self.para = config.parameters()
        self.para.setBuildID(self.buildID)
        self.features_path = self.para.get('feature_path')

        self.target_feature_map = self.para.get_executor(runner=self.executor)

        if None == self.target_feature_map:
            print "No feature map list found for executor: " + self.executor
            exit(0) # Execution exits on feature-list non found.

        target_list = self.target_feature_map.keys()
        if 1 == len(target_list):
            self.features = self.target_feature_map[target_list[0]]
        else:
            print "Unsupported multiple machine for a single runner!! Exist NOW" + len(target_list).__str__()
            exit(10)

        #register execution ID remotely if buildID is set
        if self.buildID != None:
            #to have executor started randomly time wise to have executionID correctly registered.
            start_sleep = random.uniform(1,6)
            print "sleep::: " + str(start_sleep)
            time.sleep(int(start_sleep))
            self.para.registerExecutionId()


    def pre_process(self):
        self.log_path = self.para.get('log_path')
        os.system('sudo rm -rf ' + self.log_path + os.sep + r'*')
        self.start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        #self.ver = infoCollect.get_microcode_version(self.executor)
        self.ver = ""

    def post_process(self):
        self.end_time = time.strftime('%Y-%m-%d %H:%M:%S')
        #result_proc = resultProc.resultProc(self.log_path + os.sep+ 'result.log',self.start_time, self.end_time, self.para.suite_ID)
        #result_proc.run()
        #poster.run(self.log_path, self.para.suite_ID, self.start_time, self.end_time, self.ver)
        #trigger execution statistics again when execution is finished.
        if self.target_feature_map != None:
            poster.triggerExeStatistics()

    def run_tcs_by_features(self):

        currPath = os.getcwd()

        print "Current Path: " + currPath

        #add by luoshu
        select_features = []
        case_path = self.para.get('case_path')

        jobName = currPath.split('/')[-3][:-7]

        isFileExist = os.path.exists(case_path+"/"+jobName+"/case_list.txt")
        if isFileExist:
            for line in open(case_path+"/"+jobName+"/case_list.txt"):
                if line.split('/')[0] not in select_features:
                    select_features.append(line.split('/')[0])

        for f in self.features:
            if isFileExist and f not in select_features:
                continue
            fp = self.features_path + os.sep + f
            if not os.path.isdir(fp):
                print "Directory " + fp + " doesn't exist, please check !!!!@@@@@@@@"
                continue
            print "List Directory " + fp + " now to get executable python test cases!"
            files = os.listdir(fp)
            modules = []
            for i in files:
                if re.match('^Test.*\.py$', i):
                    modules.append(i.split('.')[0])
            if len(modules) == 0:
                print "Test file " + i + "contains no executable modules, pleaes check !!!!!@@@@@@"
                continue
            else:
                print "Executable module in file " + i + " contains " + str(modules)
            abfp = os.path.abspath(fp)
            sys.path.append(abfp)
            os.chdir(fp)
            logManager.global_var.feature=f
            for i in modules:

                try:
                    xivtest.main(module = i)
                except xivtest.Finished_MTC, e:
                    print logManager.global_var.cutOffLine
                    print "For %s :" % (i)
                    print e
                    print logManager.global_var.cutOffLine
                    print ""
                    time.sleep(3)
                except Exception as e:
                    print logManager.global_var.cutOffLine
                    print "Found the exception for " + i
                    print traceback.print_exc()
                    print logManager.global_var.cutOffLine
                    print ""

                #trigger statistics after feature-module execution
                poster.triggerExeStatistics()

            logManager.global_var.feature='Unknown'
            sys.path.remove(abfp)
            os.chdir(currPath)

    def run(self):
        self.pre_process()
        self.run_tcs_by_features()
        self.post_process()
        

if __name__=="__main__":
    print 'Argument List:', str(sys.argv)
    #sys.argv is used to differentiate the run type - according to the listed feature list or orderedFeatureList
    if 2 > len(sys.argv) :
        print "Usage: run_tcs.py Runner BuildID"
        exit(1)
    buildID = sys.argv[1]
    runner = sys.argv[2]
    print "Selected Runner is " + runner + " with buildID: " + buildID
    run_obj = run_tcs(buildID=buildID,executor=runner)
    run_obj.run()
    print "Finished to run all test cases"
    print logManager.global_var.cutOffLine

