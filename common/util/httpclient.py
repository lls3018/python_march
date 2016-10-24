
import httplib



__author__ = 'Peng Shi'

class httpclient():

    def __init__(self, serverIP=None):

        self.req_hdr = httplib.HTTPConnection(serverIP)
        self.selector = ''

    def post(self,headerhash={}):
        self.req_hdr.putrequest('POST',self.selector)
        for k,v in headerhash.items():
            self.req_hdr.putheader(k,v)
        self.req_hdr.endheaders()
        self.req_hdr.send("")
        res = self.req_hdr.getresponse()
        print res.status, res.reason
        return res

    def get(self, headerhash={}):
        self.req_hdr.putrequest('GET',self.selector)
        for k,v in headerhash.items():
            self.req_hdr.putheader(k,v)
        self.req_hdr.endheaders()
        self.req_hdr.send("")
        res = self.req_hdr.getresponse()
        print res.status,res.reason
        return res

    def setSelector(self,selector=''):
        self.selector = selector

    def getHandler(self):
        return self.req_hdr