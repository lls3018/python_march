import config
import httpclient
import sys

__author__ = 'Peng Shi'

class ManualTriggerStatistic:

    def __init__(self,httpServer):
        self.httphdler = httpclient.httpclient(serverIP=httpServer)

    def triggerStatistic(self,executionID):

        if None == executionID:
            return
        resultHash = {"Oprand":"Statistic",
                    "executionID":executionID}
        self.httphdler.post(resultHash)


if __name__=="__main__":

    print 'Argument List:', str(sys.argv)
    #sys.argv is used to differentiate the run type - according to the listed feature list or orderedFeatureList
    if 2 > len(sys.argv) :
        print "Usage: manualTriggerStatistic.py <IP:Port><ExecutionID>"
        exit(1)
    executionID = sys.argv[2]
    httpServer = sys.argv[1]
    mT_instance = ManualTriggerStatistic(httpServer)
    mT_instance.triggerStatistic(executionID)
