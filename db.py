# -*- encoding: utf-8 -*-

from os import path

class Db():
	def __init__(self, filename):
		self.filename = filename
		self.data = []
		self.load()
	
	def load(self):
		if(path.exists(self.filename) and path.isfile(self.filename)):
			with open(self.filename, 'r') as f:
				for line in f.readlines():
					if(line != '\n' and line != '\r'):
						self.data.append(line)

	''' 追加记录 '''
	def add(self, obj):
		if self.exists(obj) == False:
			self.data.append(obj)
			with open(self.filename, 'a+') as f:
				f.writelines(obj+'\n')
				f.flush()
				print('Added history ' + obj)

	def exists(self, obj):
		if(self.data.count(obj))>0:
			return True
		else:
			return False