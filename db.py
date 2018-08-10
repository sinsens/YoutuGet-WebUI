# -*- coding: utf-8 -*-

from os import path

class Db():
	def __init__(self, filename='db.json'):
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
	def add(self, url):
		if(self.data.count(url+'\n'))>0:
			return False #记录已存在
		else:
			with open(self.filename, 'a+') as f:
				f.writelines(url+'\n')
				f.flush()
				f.close()
				print('添加到记录 ' + url)
				self.data.append(url+'\n')
				return True
			return False


''' 自主测试 '''

if __name__ == '__main__':
	db = Db()
	print(db.add('https://github.com/sinsens/baiduyuyin_hecheng.git'))
	input()
