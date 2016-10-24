class	PostProcess:
	def getSyslogFail(self,path,start_time, end_time):
		pass
	
	def processFail(self):
		pass
		
	def processPass(self):
		pass
		
	def processAll(self):
		pass
	
	def	__call__(self, status,path,start_time, end_time):
		self.processAll()
		if status != 'pass':
			self.getSyslogFail(path,start_time, end_time)
			self.processFail()
		else:
			self.processPass()
			
		
		