#!/usr/bin/python2.7
import os
import time
import sys
from optparse import OptionParser

def usage():
    usage_str = """
    Usage: %s getdirlist
    """ % (sys.argv[0])
    return usage_str

def getdirlist(dirname):
    if not os.path.isdir(dirname):  
        print ("Directory is wrong")
        return False   
               
    fout=file('out.txt','w')
    filelist=[]
    
    for i in os.listdir(dirname):
        filelist.append(i+'\n')
    
    fout.writelines(filelist)
    fout.close()
    print "The result is in: out.txt"  
    return True
    
if __name__ == "__main__":
    parser = OptionParser(usage = usage())

    parser.add_option("-p", "--path", action="store", dest="dirname", help="The dirname is the path dir we need get get all file name list")

    (options, args) = parser.parse_args(sys.argv)
    
    if not options.dirname:
        print "the dirname is needed"
        sys.exit(1)
    if not getdirlist(options.dirname):
      	print "get the dir list name failed"
    	sys.exit(1)

