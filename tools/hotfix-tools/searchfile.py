#!/usr/bin/python2.7
import os
import commands
import sys
from optparse import OptionParser


def usage():
    usage_str = """
    Usage: %s search all files
    """ % (sys.argv[0])
    return usage_str
    
def searchfile(filename,searchpath):
    if not os.path.isfile(filename):  
        print ("file is not exist")
        return False

    fout=file("result.txt",'w')
    filelist=[]

    fout2=file("result2.txt",'w')
    filelist2=[]

    f = open(filename)
    line = f.readline()
    while line:
        sys.stdout.write("-")
        sys.stdout.flush()
        
        cmd = 'find %s -name %s' % (searchpath ,line.strip())
        status, output = commands.getstatusoutput(cmd)
        if output=="":          
            filelist.append(line.strip()+" , "+"***NOT FOUND***"+'\n')
            filelist2.append("***NOT FOUND***"+'\n')
        else:           
            filelist.append(line.strip()+" , "+output.replace('\n',"-----")+'\n')
            filelist2.append(output.replace('\n',"-----")+'\n')
        line = f.readline()
    f.close()
    fout.writelines(filelist)
    fout.close()
    fout2.writelines(filelist2)
    fout2.close()
    print  '\n'+"the result is in: result.txt and result2.txt"
    
    return True


if __name__ == "__main__":
    parser = OptionParser(usage = usage())

    parser.add_option("-f", "--filepath", action="store", dest="filepath", help="The filepath is the filenamelist we need to search")

    parser.add_option("-p", "--searchpath", action="store", dest="searchpath", help="The searchpath is the path where we need to search")
    
    (options, args) = parser.parse_args(sys.argv)

    if not options.filepath:
        print "the input filepath is needed"
        sys.exit(1)

    if not options.searchpath:
        print "the searchpath is needed"
        sys.exit(1)
        
    if not searchfile(options.filepath,options.searchpath):
        print "the search is failed"
        sys.exit(1)
