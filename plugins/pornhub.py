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
				print("�޷�����Ŀ¼��", self.workdpath, "\n����Ȩ���Ƿ���ȷ")
		print("Pornhub����Ŀ¼:", workdpath)

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
					break  # �������˽ϸ߷ֱ��ʵ���Ƶ ������ѭ��
				except Exception as err:
					print(err)

	def download(self, url, name, filetype):
		print(url, name)
		filepath = self.workdpath+'/%s.%s' % (name, filetype)
		if os.path.exists(filepath):
			print('�ļ��Ѵ��ڣ�' % (filepath))
			return
		urllib.request.urlretrieve(url, '%s' % (filepath))
		print('������ %s' % (filepath))