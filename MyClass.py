# -*- encoding: utf-8 -*-
from os import system
import threading
from flask import render_template
from os import path
import os
from flask import request
import sys
import time


def now():
	return time.time()

class Server():
	def __init__(self, dirpath):
		self.homeroot = dirpath+'/static/'
		self.chk(dirpath)
	
	''' 目录检查 '''
	def chk(self, dirpath):
		# 检查读写
		if path.exists(self.homeroot) and path.isdir(self.homeroot):
			pass
		else:
			try:
				os.mkdir(self.homeroot)
			except:
				return "File IOError"
		print("\n\n\n")
		print("Working directory:", dirpath)
		print("File Downloaded and saved directory:", self.homeroot)
		print("\n")

	def index(self):
		mylist = self.list()
		return render_template('index.html', mylist = mylist)

	def go(self):
		url = request.form['url']
		threading.Thread(target = self.down, args=([url])).start()
		ip = request.remote_addr
		print(ip,": Get file from ",url)
		return self.index()

	def fileinfo(self, filepath):
		filepath = self.homeroot + filepath
		if path.exists(filepath) and path.isfile(filepath):
			return path.basename(filepath), path.getsize(filepath), os.stat(filepath).st_mtime
		else:
			return None

	def list(self):
		flist = []
		for i in os.listdir(self.homeroot):
			finfo = self.fileinfo(i)
			size = finfo[1]
			date = time.localtime(finfo[2])
			date = time.strftime("%Y-%m-%d %H:%M:%S",date)
			if size>(1024*1024*1024):
				size = str(round(size/1024/1024/1024,2))+"GB"
			elif (size)>(1024*1024):
				size = str(round(size/1024/1024,2))+"MB"
			else:
				size = str(round(size/1024,2))+"KB"
			flist.append({'filename':finfo[0], 'size':size, 'date':date})
		return (flist)

	def down(self, url):
		# 判断URL
		if(len(url)<15):
			return
		# 安全过滤
		if ";" in url:
			return
		
		try:
			if("youtube.com" in url):
				print("Downloding video from Youtube, this thread will switch work dir to ", self.homeroot)
				os.chdir(self.homeroot)
				system('youtube-dl %s' % (url))
			else:
				system('you-get -o %s %s' % (self.homeroot, url))
		except Exception:
			print("Some problem happend -_-||")
			raise

	def play(self, filename):
		return render_template('play.html', filename = filename)