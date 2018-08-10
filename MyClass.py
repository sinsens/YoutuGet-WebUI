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

	''' Ŀ¼��� '''
	def chk(self, workpath):
		# ����д
		if path.exists(self.homeroot) and path.isdir(self.homeroot):
			pass
		else:
			try:
				os.mkdir(self.homeroot)
			except:
				return "�ļ���д����"
		print("\n\n\n")
		print("����Ŀ¼:"+workpath)
		print("�ļ����ر���Ŀ¼:"+self.homeroot)
		print("\n")

	def index(self):
		workpath = request.args.get('dir')
		if(workpath) == None or ".." in workpath:
			workpath = ''
		mylist = self.getlist(workpath)
		return render_template('index.html', mylist = mylist, workpath = workpath, freeSize = self.freeSize())

	def go(self):
		url = request.form['url']
		
		if url=="reload":#���¼������ݿ�
			self.db = Db(self.workpath + '/db.json')
			print("���¼�����ʷ���ݿ�")
		elif(len(url)<10):#�ж�URL
			pass
		elif ";" in url or '&&' in url:#��ȫ����
			pass
		elif self.db.add(url):#�Ƿ����ع�
			ip = request.remote_addr
			print(ip,": �������� ",url)
			threading.Thread(target = self.down, args=([url])).start() # ���������߳�
		else:
			print('��ʷ�������Ѵ��ڸ�URL��ȡ������')
		return self.index()

	def fileinfo(self, filepath):
		#��֤�ļ�
		if path.exists(filepath) and path.isfile(filepath):
			return path.basename(filepath), path.getsize(filepath), os.stat(filepath).st_mtime
		else:
			#Ŀ¼����-1
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
				print(("�� %s ��¡����" % url), self.homeroot)
				os.chdir(self.homeroot)
				filename = url.split('/')[-1].replace('.git','')
				save_filename = (filename+'.tar.gz')
				cmd = ('git clone %s && tar -czf %s %s && rm -rf %s' % (url, save_filename, filename, filename))
				system(cmd)
			elif("youtube.com/" in url):
				print("��Youtube������Ƶ, ���浽��", self.homeroot)
				os.chdir(self.homeroot)
				system('youtube-dl %s' % (url))
			elif("pornhub.com/" in url):
				p = Pornhub(self.homeroot)
				p.detail_page(url)
			else:
				system('you-get -o %s %s' % (self.homeroot, url))
		except Exception:
			print("������һЩ���� -_-||")
			raise

	def play(self, filename):
		workpath = request.args.get('dir')
		if(workpath) == None:
			workpath = ''
		return render_template('play2.html', filename = filename, workpath = workpath)


	''' ��ȡ����ʣ��ռ� 
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