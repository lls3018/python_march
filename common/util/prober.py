import os



__author__ = 'Peng Shi'
authorID = "ships@cn.ibm.com"

class prober(object):

    def ping(self, hostname):
        if os.name == "nt": countOption = "-n"
        else: countOption = "-c"

        response = os.system("ping " + countOption + " 1 " + hostname)

        #if response == 0:
        #    print hostname, 'is up!'
        #else:
        #    print hostname, 'is down!'

        return response


    def testMethod(self):
        self.ping()


if __name__ == "__main__":
    testobject = prober()
    print os.name
    if testobject.ping("9.115.249.158") == 0: print 'system is pingable'
