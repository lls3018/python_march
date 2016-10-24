import os, re, time, sys, traceback
import xivtest, logManager, config


__author__ = 'Peng Shi'
authorID = "ships@cn.ibm.com"

"""
The Class/Function is used to query existed test case lise with print out according to module
"""

class queryTCList:

    def __init__(self, option=["FULLLIST"]):
        ##option is non-empty
        self.runType = option
        self.para = config.parameters()

    def query(self):
        currPath = os.getcwd()
        features_path = self.para.get('feature_path')

        #replace listed feature list with predefined feature list to control order of run
        features = os.listdir(features_path)

        for f in features:


            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

            print "Feature ---------------------------- " + f

            fp = features_path + os.sep + f
            if not os.path.isdir(fp):
                print "Directory " + fp + "doesn't exist, please check !!!!@@@@@@@@"
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
                    xivtest.main(module = i, parseMode="Query")
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
            logManager.global_var.feature='Unknow'
            sys.path.remove(abfp)
            os.chdir(currPath)



if __name__=="__main__":

    run_obj = queryTCList()
    run_obj.query()

