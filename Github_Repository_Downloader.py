import platform, time, re
from urllib.request import urlopen, build_opener, HTTPCookieProcessor
if platform.platform().startswith("Windows"):
	import ctypes
	ctypes.windll.kernel32.SetConsoleTitleW("Github Repository Downloader")


def dlUrl(url):
	res = urlopen(url)
	info = res.headers['Content-Disposition']
	if info and info.lower() != 'attachment;':
		fileName = res.headers['Content-Disposition'].split('=')[1].replace('"', '')
	else:
		fileName = url.split('/')[-1].replace('%20', ' ')
	fileSize = res.length
	chunkSize = 1024
	with open(fileName, 'wb') as fileDl:
		start = time.time()
		count = 0
		while True:
			part = res.read(chunkSize)
			if not part:
				break
			fileDl.write(part)
			count += 1
			if time.time() - start > 1:
				print('downloading speed: {} KBPS'.format(count))
				count, start = 0, time.time()
	return f'{fileName} downloaded.'


ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
opener = build_opener(HTTPCookieProcessor)
opener.addheaders = [('User-agent', ua)]
while True:
	url = input('enter your github repository url: ')
	responce = opener.open(url, timeout=5)
	page = responce.read().decode('utf-8')	
	regex = re.compile('href="(.+\.zip)">')
	url = regex.findall(page)
	if url:
		url = 'https://github.com' + url[0]
	else:
		print('not found')
		continue
	print(dlUrl(url))