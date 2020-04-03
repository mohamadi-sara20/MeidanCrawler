import requests
from lxml import html
import re
import time
import json
import os.path
import os
import wget
import time

#http://sharghdaily.com/fa/main/page
#http://sharghdaily.com/fa/main/page/6107/1
#div class=l30_main -> select -> option values

path = os.getcwd()

error_log = open('failure.log', 'w')

req = requests.get("http://sharghdaily.com/fa/main/page")
tree = html.fromstring(req.content)
numbers = tree.xpath('//option/@value')
issues =  tree.xpath('//option')
start = 99999999
		
for issue in issues:
	time.sleep(5)
	number = issue.get('value')
	date = issue.text.split('-')[0].strip()

	if int(number) > start:
		continue
	if not os.path.exists(number):
		os.mkdir(number)
	print('------------- {} -----------'.format(number))
	url = "http://sharghdaily.com/fa/main/page/{}/1/".format(number)
	req = requests.get("http://sharghdaily.com/fa/main/page")
	tree = html.fromstring(req.content)
	titrs = tree.xpath('//div[@id="divTitrs"]')
	if len(titrs) == 0:
		print("No titr {}".format(number))
		continue
	links = titrs[0].xpath('a[@class="RowStyle"]/@href')
	if (links):
		print('{} documents'.format(len(links)))
	else:
		print('no link in issue {} {}'.format(number, date))
	for link in links:
		time.sleep(1)
	# from: http://sharghdaily.com/fa/Main/Detail/2848/%D8%AF%D9%88-%D8%B3%D9%86%D8%A7%D8%B1%DB%8C%D9%88%D8%8C-%D8%AF%D9%88-%D8%AA%D8%AD%D9%84%DB%8C%D9%84
	# to: http://sharghdaily.com/1391/11/14/Main/RTF/SharghNewsPaper_2849.rtf
		link = 'http://sharghdaily.com/{}'.format(link)
		doc_search = re.search('Main/Detail/(.*)/', link, re.IGNORECASE)
		if not doc_search:
			print("No document number in link {}".format(link))
			continue
		doc = doc_search.group(1)

		url = "http://sharghdaily.com/{}/Main/RTF/SharghNewsPaper_{}.rtf".format(date, doc)
		#requests.get(link)
		time.sleep(1)
		# req = requests.get(url)
		# content = req.content
		# if str(content).startswith('روزنامه شرق'):
		# 	open('{}/{}.txt'.format(number, doc), 'wb').write(req.content)
		# else:
		# 	error_log.write(url+'\n')
		
		try:
			wget.download(url, out='{}\\{}\\{}.txt'.format(path,number,doc))
		except:
			error_log.write('document {} download failed - {}'.format(doc, url))
			pass

	
	

