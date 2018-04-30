# -*- encoding: utf-8 -*-

from flask import render_template, request
from os import path
from os import system
import threading
import os
import sys
import time
from db import Db

def now():
	return time.time()

class Server():
	def __init__(self, workpath):
		self.homeroot = workpath+'/static/'
		self.chk(workpath)
		self.db = Db(workpath + '/db.json')

	''' 目录检查 '''
	def chk(self, workpath):
		# 检查读写
		if path.exists(self.homeroot) and path.isdir(self.homeroot):
			pass
		else:
			try:
				os.mkdir(self.homeroot)
			except:
				return "File IOError"
		print("\n\n\n")
		print("Working directory:"+workpath)
		print("File download and save directory:"+self.homeroot)
		print("\n")

	def index(self):
		workpath = request.args.get('dir')
		if(workpath) == None:
			workpath = ''
		mylist = self.getlist(workpath)
		return render_template('index.html', mylist = mylist, workpath = workpath)

	def go(self):
		url = request.form['url']
		# 判断URL
		if(len(url)<15):
			return self.index()
		# 安全过滤
		if ";" in url or '&&' in url:
			return self.index()
		# 是否下载过
		if self.exists(url) == True:
			print('This url was already exist in database.')
			return self.index()
		ip = request.remote_addr
		print(ip,": Get file from ",url)
		# 启动下载线程
		threading.Thread(target = self.down, args=([url])).start()
		return self.index()

	def fileinfo(self, filepath):
		#验证文件
		if path.exists(filepath) and path.isfile(filepath):
			return path.basename(filepath), path.getsize(filepath), os.stat(filepath).st_mtime
		else:
			#目录返回-1
			return path.basename(filepath), -1, os.stat(filepath).st_mtime

	def getlist(self, filepath=''):
		if path.exists(self.homeroot+filepath)==False:
			return None
		filepath = self.homeroot+filepath+'/'
		flist = []
		for i in os.listdir(filepath):
			nowfilepath = filepath + i
			finfo = self.fileinfo(nowfilepath)
			size = finfo[1]
			date = time.localtime(finfo[2])
			date = time.strftime("%Y-%m-%d %H:%M:%S",date)
			if size>(1024*1024*1024):
				size = str(round(size/1024/1024/1024,2))+"GB"
			elif (size)>(1024*1024):
				size = str(round(size/1024/1024,2))+"MB"
			elif(size>0):
				size = str(round(size/1024,2))+"KB"
			else:
				size = size
			flist.append({'filename':finfo[0], 'size':size, 'date':date})
		return (flist)

	def down(self, url):
		try:
			if("youtube.com" in url):
				print("Downloding video from Youtube, this thread will switch work dir to ", self.homeroot)
				os.chdir(self.homeroot)
				system('youtube-dl %s' % (url))
			else:
				system('you-get -o %s %s' % (self.homeroot, url))
		except Exception:
			print("Some problem happened -_-||")
			raise

	def play(self, filename):
		workpath = request.args.get('dir')
		if(workpath) == None:
			workpath = ''
		return render_template('play2.html', filename = filename, workpath = workpath)

	''' 检查是否下载过 '''
	def exists(self, url):
		if(self.db.exists(url)):
			return True
		else:
			self.db.add(url)
			return False