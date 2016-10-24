#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys,re,struct,os,signal,time
sys.path.append('../../common/util')
import Env
import Connection

def LDAP_server_config (XIV_IP):
	'''config ldap server'''
	print Env.id_rsa
	SSH = Connection.Connection(
									host = XIV_IP, 
									username = "root",
									private_key = Env.id_rsa
								)
        
	'''example for remote command invoation'''
	SSH.execute("xcli.py ldap_mode_set mode=Inactive -y;")
	SSH.execute("xcli.py --user xiv_development --password x1vD3v ldap_config_reset;")
	SSH.execute("xcli.py ldap_add_server fqdn=test.xiv.ibm.com address=9.115.249.189 base_dn=cn=users,dc=test,dc=xiv,dc=ibm,dc=com;")
	SSH.execute("xcli.py ldap_config_set user_name_attrib=userPrincipalName xiv_group_attrib=memberOf user_id_attrib=sAMAccountName xiv_user=\"cn=gui10,cn=users, dc=test,dc=xiv,dc=ibm,dc=com\" xiv_password=\"x1vD3v_#10\" use_ssl=no storage_admin_role=\"cn=XIVAdmins,ou=XIVLab,dc=test,dc=xiv,dc=ibm,dc=com\" read_only_role=\"cn=XIVOpers,ou=XIVLab,dc=test,dc=xiv,dc=ibm,dc=com\" server_type=\"MICROSOFT ACTIVE DIRECTORY\";")
	SSH.execute("xcli.py ldap_mode_set mode=Active -y;")
		
		
	result = SSH.execute("xcli.py ldap_list_servers | grep \"test.xiv.ibm.com\" | awk {'print $1'}")[0].strip()
	if result != 'test.xiv.ibm.com':
		self.log.debug("LDAP server configuration failed!") 
		exit(1)
		
        
	self.log.debug("LDAP server configuration finished successfully!")
	SSH.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: ',sys.argv[0],'XIV_IP'
		sys.exit(1)
	else:
		XIV_IP = sys.argv[1]
	
	LDAP_server_config (XIV_IP)