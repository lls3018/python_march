#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import time

from common.util import pexpect

sys.path.append('../../common/util')
import Env
import Connection

fc_wwpn_initiator = None
fc_wwpn_target = None




def wwpn_format_change(wwpn):
	temp = wwpn
	re = '' 
	for i in range(0,len(temp),2):
		re+=temp[i:i+2]
		re+=":"
	return re[0:-1]

	
def get_fc_wwpn(local_xiv_ip):
	SSH = Connection.Connection(
										host = local_xiv_ip, 
										username = "root",
										private_key = Env.id_rsa
								)
	
	status_check = SSH.execute("xcli.py fc_port_list | grep OK | grep Initiator | grep Online | awk {'print $4'} | wc -1")[0].strip()
	if status_check == '0':
		print "There is no online initiator port on" + local_xiv_ip
		return 1
	fc_wwpn_initiator_1 = SSH.execute("xcli.py fc_port_list | grep OK | grep Initiator | awk {'print $4'} | head -1")[0].strip()
	print fc_wwpn_initiator_1
	
	zone_config.fc_wwpn_initiator = wwpn_format_change(fc_wwpn_initiator_1)
	
	status_check = SSH.execute("xcli.py fc_port_list | grep OK | grep Target | grep Online | awk {'print $4'} | wc -1")[0].strip()
	if status_check == '0':
		print "There is no online target port on" + local_xiv_ip
		return 1
	fc_wwpn_target_1 = SSH.execute("xcli.py fc_port_list | grep OK | grep Target | awk {'print $4'} | head -1")[0].strip()
	
	zone_config.fc_wwpn_target = wwpn_format_change(fc_wwpn_target_1)
	SSH.close()



def zone_create(master_id, slave_id, master_initiator_wwpn, master_target_wwpn, slave_initiator_wwpn, slave_target_wwpn):
	time.sleep(25)
	SSH = Connection.Connection(
										host = "9.115.249.160", 
										username = "root",
										password = "passw0rd"
								)
	#change "-" to "_"
	temp = master_id
	
	for i in range(0,len(temp)):
		if temp[i] == '-':
			temp = temp[:i] + '_' + temp[i+1:]
		
	
	master_id = temp
	
	temp = slave_id
	
	for i in range(0,len(temp)):
		if temp[i] == '-':
			temp = temp[:i] + '_' + temp[i+1:]
	
	slave_id = temp
	
	SSH.execute("cfgtransabort")
	time.sleep(10)
	
	#check_duplicate = SSH.execute("/fabos/link_bin/zoneShow | grep %s_%s | wc -l" % (master_id, slave_id))[0].strip()
	#if check_duplicate == '1':
	#	print "Zone already exists."
	#cmd="/fabos/link_abin/zoneCreate \"%s_%s\",\"%s;%s;%s;%s\"" % (master_id, slave_id, master_initiator_wwpn, master_target_wwpn, slave_initiator_wwpn, slave_target_wwpn)
	#zone_create = SSH.execute(cmd) #[0].strip()

	
	SSH.close()
	
	foo = pexpect.spawn('ssh root@9.115.249.160')
	foo.logfile = sys.stdout
	index = foo.expect(["(?i)password", pexpect.EOF, pexpect.TIMEOUT])
	if index == 0:
		foo.sendline('passw0rd')
		index = foo.expect(["(?i)IBM_2498_B40_XIV_QA_1", pexpect.EOF, pexpect.TIMEOUT])
		if index != 0:
			print "ssh to switch error, exit..."
			exit(1)
			
	foo.sendline("/fabos/link_abin/zoneCreate \"%s_%s\",\"%s;%s;%s;%s\"" % (master_id, slave_id, master_initiator_wwpn, master_target_wwpn, slave_initiator_wwpn, slave_target_wwpn))
	index = foo.expect(["duplicate name", pexpect.EOF, pexpect.TIMEOUT])
	print index
	
	foo.sendline("/fabos/link_abin/cfgadd \"cfg\", \"%s_%s\"" % (master_id, slave_id))
	time.sleep(10)
	
	foo.sendline('/fabos/link_abin/cfgSave')
	index = foo.expect(["(?i)Do you want to save Defined zoning configuration only", pexpect.EOF, pexpect.TIMEOUT])
	if index == 0:
		foo.sendline('yes')
		index = foo.expect(["(?i)Updating flash", pexpect.EOF, pexpect.TIMEOUT])
		if index != 0:
			print "Save zone configure error, exit..."
			exit(1)
			
	foo.sendline('cfgEnable cfg')
	
	index = foo.expect(["(?i)Do you want to enable 'cfg' configuration", pexpect.EOF, pexpect.TIMEOUT])
	if index == 0:
		foo.sendline('yes')
		index = foo.expect(["(?i)Updating flash", pexpect.EOF, pexpect.TIMEOUT])
		if index != 0:
			print "Failed to enable configure, exit..."
			exit(1)
	foo.sendline('exit')
	
	SSH = Connection.Connection(
										host = "9.115.249.160", 
										username = "root",
										password = "passw0rd"
								)
								
	check_success = SSH.execute("/fabos/link_bin/zoneShow | grep %s_%s | wc -l" % (master_id, slave_id))[0].strip()
	if check_success == '0':
		print "Create zone failed, exit..."
		exit(1)
		
	print "Zone created successfully!"
	SSH.close()

def zone_config(master_id, master_ip, slave_id, slave_ip):
	print "start zone config"
	print master_id, master_ip, slave_id, slave_ip
	a = get_fc_wwpn(master_ip)
	if a == 1:
		print "FC port problem on master machine, can't config zone"
		return 1
	fc_wwpn_master_initiator = zone_config.fc_wwpn_initiator
	fc_wwpn_master_target = zone_config.fc_wwpn_target
	print master_ip, fc_wwpn_master_initiator,fc_wwpn_master_target
	
	a = get_fc_wwpn(slave_ip)
	if a == 1:
		print "FC port problem on slave machine, can't config zone"
		return 1
	fc_wwpn_slave_initiator = zone_config.fc_wwpn_initiator
	fc_wwpn_slave_target = zone_config.fc_wwpn_target
	print slave_ip, fc_wwpn_slave_initiator, fc_wwpn_slave_target
	
	
	
	if not fc_wwpn_master_initiator or not fc_wwpn_master_target or not fc_wwpn_slave_initiator or not fc_wwpn_slave_target:
		print "There is fc port problem. Can't create mirror under this circumstance."
		exit(1)
		
	zone_create(master_id, slave_id, fc_wwpn_master_initiator, fc_wwpn_master_target, fc_wwpn_slave_initiator, fc_wwpn_slave_target)
	
if __name__ == '__main__':
	if len(sys.argv) != 5:
		print 'Usage: ',sys.argv[0],'master_id master_ip slave_id slave_ip'
		sys.exit(1)
	else:
		master_id = sys.argv[1]
		
		master_ip = sys.argv[2]
		slave_id = sys.argv[3]
		
		slave_ip = sys.argv[4]
		
	
	zone_config(master_id, master_ip, slave_id, slave_ip)
