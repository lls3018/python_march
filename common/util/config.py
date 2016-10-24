from patterns import Singleton
import httplib, os
import httpclient


class Config_Failure(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class parameters(Singleton):
    def __init__(self):
        Singleton.__init__(self)

        self.http_server = os.environ.get('HTTPServer')
        self.suite_ID = os.environ.get('Suite_ID')
        self.config_file = os.environ.get('Config_File')
        self.buildID = None
        self.executionID = None
        self.remote_paras = []
        self.local_paras = []
        self.httpclient = None
        if self.http_server is not None:
            print "HTTPServer is: " + self.http_server
            self.httpclient = httpclient.httpclient(self.http_server)
        self._initializeParaSet()


    def _initializeParaSet(self):
        if self.config_file is not None:
            print "Read Config from Local configuration file: " +  self.config_file
            f = open(self.config_file, 'r')
            self.local_paras = eval(f.read())
        else:
            print "Config_File Not Set ======"

        if self.http_server is not None:
            self._get_remote_paras()

        else:
            print "HTTPServer Not Set ======"

    def _get_remote_paras(self):
        print "in _get_remote_paras"
        if 1 < len(self.remote_paras):
            print "remote_paras not None, Return Now"
            print self.remote_paras
            print len(self.remote_paras)
            return

        print "Suite_ID is set to: " + self.suite_ID
        print "HTTPServer is set to: " + self.http_server
        #conn = httplib.HTTPConnection(self.http_server)
        #conn.request("GET", "/" + self.suite_ID + "/config?get=config")
        self.httpclient.setSelector("/" + self.suite_ID + "/config?get=config")
        response = self.httpclient.get({})
        self.httpclient.setSelector('')
        #response = conn.getresponse()
        if response.status != 200:
            raise Config_Failure("Get parameters from Server failure(%s, %s)."(response.status, response.reason))
        data = response.read()
        print "User Parameters:"
        print data
        self.remote_paras = eval(data)


    def get(self, para):

        if para in self.local_paras:
            if self.local_paras[para] is not None:
                #print "para: " + para + " found in local configuration"
                return self.local_paras[para]
            #else:
                #print "para: " + para + " is empty in local configuration"
        #else:
            #print "para: " + para + " not set in local configuration"

        if para in self.remote_paras:
            if self.remote_paras[para] is not None:
                #print "para: " + para + " found in remote configuration"
                return self.remote_paras[para]
            #else:
                #print "para: " + para + " is empty in remote configuration"
        #else:
            #print "para: " + para + " not set in remote configuration"

        print "para: " + para + " NOT FOUND, Please Check!"
        return None


    def get_executor(self,featureName=None, runner=None):
        #fetch two parameters - pair_ip_of_target_host & features_mapped_to_target
        ftm_string = self.get("features_mapped_to_target").split(";")
        thm_string = self.get("pair_ip_of_target_host").split(";")
        designated_target = ""
        designated_host = ""
        designated_runner = ""

        #fetch executor set for feature if featureName is not None
        if featureName is not None and runner is None:
            print "feature executor set for feature: " + featureName
            found = False
            for i in ftm_string:

                designated_target, f_list = i.split(":")
                for j in f_list.split(","):
                    #print j
                    if featureName == j:
                        found = True
                        print "Feature Found: " + featureName
                        break

                if True == found:
                    print "Target System Found: " + designated_target
                    break

            if False == found:
                print "Target System Not Found for feature: " + featureName
                return None
            #print "d_t " + designated_target
            for m in thm_string:
                #print m
                if designated_target == m.split(":")[0]:
                    designated_runner, designated_host = m.split(":")[1].split(",")
                    break

            print "Executor for feature: " + featureName + " are:"
            print "target system: " + designated_target
            print "host: " + designated_host
            print "runner: " + designated_runner

            executor = {"target":designated_target,"host":designated_host,"runner":designated_runner}
            return executor

        elif runner is not None and featureName is None:
            print "fetch feature list for runner: " + runner
            found = False
            for m in thm_string:
                if "" == m:
                    #continue
                    print "the thm_string is " + thm_string
                designated_target, runner_host_pair = m.split(":")
                if runner == runner_host_pair.split(",")[0]:
                    print "found controlled target is :" + designated_target + " for runner:" + runner
                    found = True
                    break

            if True == found:
                for i in ftm_string:
                    if "" == i:
                        #continue
                        print "the ftm_string is " + str(ftm_string)
                    cursor_target, featureListString_per_target = i.split(":")
                    if  cursor_target == designated_target:
                        featureList_per_target = featureListString_per_target.split(",")
                        t = {designated_target: featureList_per_target}
                        print featureList_per_target
                        return t
            else:
                return None

        else:
            print "ERROR: No other scenarios supported so far..."
            return None

    def registerExecutionId(self):

        if self.buildID is None:
            print "buildID is not set, return without register ExecutionID now..."
            return
        else:
            print "The buildID is :" + self.buildID

        req_post = {'Oprand':'ExecutionIDReg', 'T_J_ID':self.buildID, 'Suite_ID': self.suite_ID}
        res = self.httpclient.post(req_post)

        self.executionID = res.getheader(name="ExecutionID")

        print "Got Execution ID from Remote DB: " + self.executionID
        return self.executionID

    def setBuildID(self,buildID):
        self.buildID = buildID

        print "Set Class Parameters BuildID to : " + self.buildID

    def gethttpclient(self):
        return self.httpclient




 