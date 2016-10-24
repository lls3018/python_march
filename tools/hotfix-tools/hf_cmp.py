# __CR__
# Copyright (c) 2008-2013 EMC Corporation
# All Rights Reserved
#
# This software contains the intellectual property of EMC Corporation
# or is licensed to EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of EMC.
# __CR__

import os
import sys
import commands
import shutil
from optparse import OptionParser


def usage():
    usage_str = """
    Usage: %s compare the tar tall 
    """ % (sys.argv[0])
    return usage_str

def compare_tarball():
    if not (os.path.exists('./temp_src') and os.path.exists('./temp_des')):
        return False
    else:
        src_dir = os.listdir(r'./temp_src')[0]
        des_dir = os.listdir(r'./temp_des')[0]
    
    cmd = 'diff -Nur %s %s' % ('./temp_src/'+src_dir ,'./temp_des/'+des_dir)
    status, output = commands.getstatusoutput(cmd)
    if status:
        print 'the tarball %s %s is not the same %s \n' % (src_dir, des_dir, output)
        return False
   
    print "the two tarball %s and %s is same" % (src_dir, des_dir)
    return True 

def uncompress(src, dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        
    path = dirname
    cmd = 'tar -xvf %s -C %s' % (src, path)
    status, output = commands.getstatusoutput(cmd)
    if status:
        print 'tar tarball into %s failed: %s \n' % (path, output)
        return False
           
    return True

if __name__ == "__main__":
    parser = OptionParser(usage = usage())

    parser.add_option("-s", "--src", action="store", dest="src_path", help="the tar src path")

    parser.add_option("-d", "--des", action="store", dest="des_path", help="the tar des path")

    (options, args) = parser.parse_args(sys.argv)
  
    if not options.src_path:
        print "the src_path is needed"
        sys.exit(1)
        
    if not options.des_path:
        print "the des_path is needed"
        sys.exit(1)
    
    if not uncompress(options.src_path,"./temp_src/"):
    	print "src tarball uncomress is failed"
    	sys.exit(1)
 
    if not uncompress(options.des_path,"./temp_des/"):
    	print "des tarball uncomress is failed"
    	sys.exit(1)
 
    if not compare_tarball():
    	 print "compare is failed"
    	 sys.exit(1)

    shutil.rmtree('./temp_src')
    shutil.rmtree('./temp_des')
    print "Success compare"
