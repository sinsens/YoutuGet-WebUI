# -*- encoding: utf-8 -*-

from flask import render_template, request
from os import path
from os import system
import threading
import os
import sys
import time
from db import Db
from plugins.pornhub import Pornhub


class Server():
	def __init__(self, workpath):
		self.workpath=workpath
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
				return "文件读写错误"
		print("\n\n\n")
		print("工作目录:"+workpath)
		print("文件下载保存目录:"+self.homeroot)
		print("\n")

	def index(self):
		workpath = request.args.get('dir')
		if(workpath) == None or ".." in workpath:
			workpath = ''
		mylist = self.getlist(workpath)
		return render_template('index.html', mylist = mylist, workpath = workpath, freeSize = self.freeSize())

	def go(self):
		url = request.form['url']
		
		if url=="reload":#重新加载数据库
			self.db = Db(self.workpath + '/db.json')
			print("重新加载历史数据库")
		elif(len(url)<10):#判断URL
			pass
		elif ";" in url or '&&' in url:#安全过滤
			pass
		elif self.db.add(url):#是否下载过
			ip = request.remote_addr
			print(ip,": 请求下载 ",url)
			threading.Thread(target = self.down, args=([url])).start() # 启动下载线程
		else:
			print('历史数据中已存在该URL，取消下载')
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
			if("github.com/" in url):
				print(("从 %s 克隆到：" % url), self.homeroot)
				os.chdir(self.homeroot)
				filename = url.split('/')[-1].replace('.git','')
				save_filename = (filename+'.tar.gz')
				cmd = ('git clone %s && tar -czf %s %s && rm -rf %s' % (url, save_filename, filename, filename))
				system(cmd)
			elif("youtube.com/" in url):
				print("从Youtube下载视频, 保存到：", self.homeroot)
				os.chdir(self.homeroot)
				system('youtube-dl %s' % (url))
			elif("pornhub.com/" in url):
				p = Pornhub(self.homeroot)
				p.detail_page(url)
			else:
				system('you-get -o %s %s' % (self.homeroot, url))
		except Exception:
			print("发生了一些问题 -_-||")
			raise

	def play(self, filename):
		workpath = request.args.get('dir')
		if(workpath) == None:
			workpath = ''
		return render_template('play2.html', filename = filename, workpath = workpath)


	''' 获取磁盘剩余空间 
	http://www.cnblogs.com/aguncn/p/3248911.html
	'''
	def freeSize(self):
		import platform
		if platform.system() == "Windows":
			import ctypes
			free_bytes = ctypes.c_ulonglong(0)
			ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(self.homeroot), None, None, ctypes.pointer(free_bytes))
			return str(round(free_bytes.value/1024/1024/1024,2))+"GB"
		else:
			st = os.statvfs(self.homeroot)
			return str(round(st.f_bavail * st.f_frsize/1024/1024/1024,2))+"GB"