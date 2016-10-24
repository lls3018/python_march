import paramiko
import threading
import getpass
import sys
import urllib
import pprint

'''
  This tool is used for checking the Israel hosts.
  Whether the hosts running iotool or not(tlib or iorate).
  And show who is running the iotool.
  Also Show the Linux Version of the host.

  Default hosts :
  all host in https://sysconf.xiv.ibm.com/hosts/reports/all/
  (include QA and UNASSIGNED,  except DEV)
'''

authorID = "wenqiz@cn.ibm.com"

hosts_ip = ("host096","host097","host114","host134","host124","host132","host011",
            "host058","host070","host140","host156","host157","host249",
            "host213","host247","host082","dhost014","lsihost059","host053","thost2-48",
            "thost3-86","thost3-116","thost4-99","ihost09")

host_none_iotool_list = []     # the host list not running iotool

class Check_host_state():
    """
    Tool for check io process (tlib and iorate)
    """
    def  ssh2(self,host_name,user,passwd,cmd):
         '''
         ssh to the host ,and run the cmd command.
         '''
         try:
             ssh = paramiko.SSHClient()
             ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
             ssh.connect(host_name  + ".xiv.ibm.com",22,user,passwd,timeout=5)
             stdin1, stdout1, stderr1 = ssh.exec_command(cmd[1])
             host_version =stdout1.readlines()[0].strip('\n')
             stdin, stdout, stderr = ssh.exec_command(cmd[0])
             owners = self.get_host_owner(host_name)
             out = stdout.readlines()
             if len(out) == 0:
                 host_none_iotool_list.append(host_name+ " [Owner: %s] [%s]"%(owners,host_version))
                 print '%s,\tOK\t%d\t[Owner : %s]\t[%s]'%(host_name,len(out),owners,host_version)
             else:
                 user_list = []
                 for line in out:
                     user_list.append(line.split(" ")[0])
                 user_list = list(set(user_list))
                 print '%s,\tOK\t%d\t[Owner: %s]\t[Running User: %s]\t[%s]'\
                       %(host_name,len(out),owners,','.join(user_list),host_version)

             ssh.close()
         except Exception, e:
             print '%s,\tError\t'%(host_name)
             print e

    def  get_host_owner(self,host_name):
         '''
         From the sysconf to check the system owner
         '''
         url = "https://sysconf.xiv.ibm.com/hosts/" +host_name+"/owners.txt"
         wp = urllib.urlopen(url)
         content = wp.read().replace("\n",",")
         return content

    def get_host_location(self,host_name):
        '''
        From the sysconf to check the system location . future use
        '''
        url = "https://sysconf.xiv.ibm.com/hosts/" +host_name+"/location.txt"
        wp = urllib.urlopen(url)
        content = wp.read().replace("\n",",")
        return content

    def check_iotool(self,iotool_name):
        '''
           Check whether the io tool process is running or not.
        '''
        io_process_name = iotool_name
        check_tlib_cmd = "ps -ef |grep %s|grep -v grep"%io_process_name
        check_host_version = "cat /etc/issue | head -n 1"   # Get the host Linux Version.
        check_cmd = [check_tlib_cmd,check_host_version]
        threads = []
        nloops = range(len(hosts_ip))

        print "----------Begin----------"
        username = "wenqiz"
        password = "Wayne^0823"
        #username = raw_input("Please input your username: ")
        #password = raw_input("Please input your password: ")
        #password = getpass.getpass('Please input your password: ')

        
        input_host_ip = raw_input("Please input specific host_ip( Direct Enter. Default check the FVT Hosts): ")
        local_hosts_ip = hosts_ip
        if input_host_ip != "":
            local_hosts_ip = input_host_ip.split(",")
            nloops = range(len(local_hosts_ip))

        for ip in local_hosts_ip:
            t=threading.Thread(target=self.ssh2, args=(ip,username,password,check_cmd),name="check_iotool")
            threads.append(t)

        for i in nloops:
            threads[i].start()
        for i in nloops:
            threads[i].join()

        print("\n-------The %s process is not running on the following list-------"%io_process_name)

        pprint.pprint(host_none_iotool_list)


if __name__=="__main__":
    process_name = raw_input("Please input the process name you want to check [iorate | tlib]: ")
    process_name = process_name.strip()
    a = Check_host_state()
    if(process_name.__eq__("iorate") or process_name.__eq__("tlib")):
        a.check_iotool(process_name)
    else:
        print "input wrong"
        exit
