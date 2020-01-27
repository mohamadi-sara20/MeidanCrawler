import requests
from lxml import html, etree
import json
import re
from bs4 import BeautifulSoup
from xml.etree import ElementTree

def getText(link):
	page = requests.get(link)
	tree = html.fromstring(page.text)
	tree = etree.ElementTree(tree)
	title = tree.xpath('//title')
	#print(title[0].text)
	# text = tree.xpath('//span[@style="font-weight: 400;"]')
	div_res = tree.xpath('//*[@id="wtr-content"]/p/span[@style="font-weight: 400;"]')
	# print(etree.tostring(div_res[0], encoding='utf8'))
	print(len(div_res))
	for i in div_res:
		print(i.text)

getText('https://meidaan.com/archive/66581')