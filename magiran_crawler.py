from lxml import html
import requests, re, os
from time import sleep

newspaper_link = 'https://www.magiran.com/newspaper/2825'
def get_first_page_news(newspaper_link):
	req = requests.get(newspaper_link)
	tree = html.fromstring(req.content)
	div = tree.xpath('//*[contains(@class, "nvol-content-body")]')[0]
	links = div.xpath('.//a/@href')
	return links

def get_year_links(archive_link):
	page = requests.get(archive_link)
	tree = html.fromstring(page.content)
	links = tree.xpath("//*[contains(@class, 'nav-link archive-year') and (contains(., '1398') or contains(., '1397') or contains(., '1396') or contains(., '1395'))]")
	hrefs = [newspaper_link + e.get('href') for e in links]
	return hrefs

def get_month_links(year_link):
	page = requests.get(link)
	tree = html.fromstring(page.content)
	links = tree.xpath('//*[contains(@class, "collapse-box")]')
	return len(links)


def get_issue_link(year_file):
	print('@@@@@@@@@@@@')

	print(year_file)

	print('@@@@@@@@@@@@')

	with open(year_file) as f:
			content = f.read()
	all_links = re.findall('href="/newspapertoc/\\d+', content)
	return all_links


def get_news_properties(news_link):
	content = ''
	page = requests.get(news_link)
	tree= html.fromstring(page.content)
	try:
		news_type = tree.xpath("//div[@class='mi-part']/span")[0].text
	except:
		news_type = 'type_unknown'
	try:
		title = tree.xpath("//*[@class='mi-title']")[0].text
	except:
		title = 'title_unknown'
	try:
		date = tree.xpath("//div[@class='col-md-6 px-0 py-2']/span")[1].text
	except:
		date = 'date_unknown'
	try:
		body = ''.join( tree.xpath("//div[@class='mi-body']")[0].itertext())
	except:
		body = 'content_unknown'
	return date + '\n-----------------------------------------\n' + news_type + '\n-----------------------------------------\n' + title + '\n-----------------------------------------\n' + body

def get_data_files_path(dirpath):
	return os.listdir(dirpath)



if __name__ == "__main__":
	
	data_dirpaths = ['shargh_data', 'etemad_data']

	for directory in data_dirpaths:
		filenames = get_data_files_path(directory)

		for f in filenames:
			print('!!!!!!!')
			print(f)
			print('!!!!!!')
			if f.startswith('.'):
				continue
			year = f.split('.')[0][-2:]
			sleep(10)
			issue_links = get_issue_link(directory + '/' + f)
			news_path = 'https://magiran.com' 
		
			for iss in issue_links:
				try:
					print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
					print(news_path + iss[6:])
					sleep(5)
					links = get_first_page_news(news_path + iss[6:])
			
					for l in links:
						head_url = news_path + l
						try:
							sleep(10)
							props = get_news_properties(head_url)
							with open('output/' + directory + '/' + year + '/' + l.split('/')[-1] + '.txt', 'w') as f:
								f.write(props)
						except:
							print('Post ' + str(l) + ' Unavailable')
				except: 
					print('First Page Not Found for' + str(iss))
					

					
					
