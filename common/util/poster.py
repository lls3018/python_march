import httplib,sys
import mimetypes
import os,zipfile
from os.path import *
import config
import httpclient

para=config.parameters()

def post_multipart(host, selector, files,suite,start_time, end_time, ver):
    content_type, body = encode_multipart_formdata(files,suite,start_time,end_time, ver)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('Oprand','RESULTLOG')
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg,headers = h.getreply()
    return "OK"#h.file.read()

def encode_multipart_formdata(files,suite_id,start_time,end_time, ver):
    LIMIT = '-'*10 + 'lImIt_of_THE_fIle_eNd_$'
    CRLF = os.linesep
    L = []

    for (key, filename, value) in files:
        L.append('--' + LIMIT)
        h1='Content-Disposition: form-data;name="%s"; filename="%s"; suite_id="%s";start_time="%s";end_time="%s";ver="%s"' % (key, filename,suite_id,start_time,end_time,ver)
        L.append(h1)
        print h1
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append('')
        L.append(value)
        L.append('--' + LIMIT + '--')
        L.append('')


    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % LIMIT
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def add_zip_folder_r( foldername, filename, type ):
    #empty_dirs=[]
    print "foldername"
    print foldername
    zip = zipfile.ZipFile( filename, type, zipfile.ZIP_DEFLATED )
    for root,dirs,files in os.walk(foldername):
#files of cur file
        print "root"
        print root
        print "dirs"
        print dirs
        print "files"
        print files
        for filename in files:
            print "compressing",(root+'/'+filename).encode("gbk")
            zip.write((root+'/'+filename).encode("gbk"))
# empty dir 
        if  len(files) == 0:
            print 'empty dir'
            zif=zipfile.ZipInfo((root+'/').encode("gbk"+"/"))
            zip.writestr(zif,"")
    zip.close()
    print "Finish compressing"
 
def walkdir(spath, mode):
    path = os.listdir(spath)  
    dir, file = [], []  
    for i in path:
        if isdir(join(spath, i)):
            dir.append(i)
        else:
            file.append(i)
    if mode == ['']:
        print spath
    else:
        for j in file:
            findout = 0
            for k in mode:
                if j[-len(k):] == k:
                    print spath
                    findout = 1
                    break
            if findout:
                break
    for k in dir:
        walkdir(join(spath, k), mode)
    return dir   
def isfiletype(mode):
    return 1	

def run(log_path, suite_id, start_time, end_time, ver):

    server_addr=para.http_server
    dirs = walkdir(log_path,'')
    filename = 'log_of_'+suite_id+'_'+'.tar'
    print "dirs"
    print dirs
    os.chdir(log_path)
    type = 'w'
    add_zip_folder_r('.', filename, type )
    '''
    count = 0
    for dir in dirs:
        type = 'a'
        if count == 0 :
            type = 'w'
        add_zip_folder_r(dir, filename, type )
        print dir
        count += 1
    '''
    #cmd = 'tar cvf '+filename+' ./*'
    #os.system(cmd)
    f=open(join(log_path,filename),'rb')
    files=[('file',filename,f.read())]
    post_multipart(server_addr,'', files,suite_id,start_time,end_time, ver)

def triggerExeStatistics():


    if para.__getattribute__("buildID") is not None:
        httphdler = httpclient.httpclient(serverIP=para.__getattribute__("http_server"))
        resultHash = {"Oprand":"Statistic",
                    "executionID":para.__getattribute__("executionID")}
        httphdler.post(resultHash)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Usage: ',sys.argv[0],'log_path suite_id start_time end_time ver'
        sys.exit(1)
    else:
        log_path=sys.argv[1]
        suite_id=sys.argv[2]
        start_time=sys.argv[3]
        end_time=sys.argv[4]
        ver=sys.argv[5]
    run(log_path, suite_id, start_time, end_time, ver)
