# copy from https://github.com/killmymates/Pornhub/blob/master/crawler.py

import json, urllib, os, requests, re
from lxml import etree

class Pornhub:
	def __init__(self, workdpath):
		self.workdpath=workdpath+"/Pornhub"
		self.headers = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
		}
		if os.path.exists(self.workdpath) == False:
			try:
				os.mkdir(self.workdpath)
			except:
				print("无法创建目录：", self.workdpath, "\n请检查权限是否正确")
		print("Pornhub下载目录:", workdpath)

	def detail_page(self, url):
		s = requests.Session()
		resp = s.get(url, headers=self.headers)
		html = etree.HTML(resp.content)
		title = ''.join(html.xpath('//h1//text()')).strip()

		js = html.xpath('//*[@id="player"]/script/text()')[0]
		tem = re.findall('var\\s+\\w+\\s+=\\s+(.*);\\s+var player_mp4_seek', js)[-1]
		con = json.loads(tem)

		for _dict in con['mediaDefinitions']:
			if 'quality' in _dict.keys() and _dict.get('videoUrl'):
				print('%s %s' % (_dict.get('quality'), _dict.get('videoUrl')))
				try:
					self.download(_dict.get('videoUrl'), title, 'mp4')
					break  # 如下载了较高分辨率的视频 就跳出循环
				except Exception as err:
					print(err)

	def download(self, url, name, filetype):
		print(url, name)
		filepath = self.workdpath+'/%s.%s' % (name, filetype)
		if os.path.exists(filepath):
			print('文件已存在：' % (filepath))
			return
		urllib.request.urlretrieve(url, '%s' % (filepath))
		print('已下载 %s' % (filepath))