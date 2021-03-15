from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import json
from selenium import webdriver
import re

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0'
options = Options()
options.add_argument("--no-sandbox")
options.add_argument('user-agent={user_agent}')
options.add_argument("--headless")
path = '/usr/bin/chromedriver'

product_ids = ['list', 'of', 'oculus', 'game', 'link']
data_to_update = []
base_url = "https://www.oculus.com/experiences/rift/"
for product_id in product_ids:
	driver = webdriver.Chrome(path, chrome_options=options)
	url = base_url + product_id

	print ('Opening new link...')
	print (url)
	try:
		driver.get(url)
		time.sleep(5)
		try:
			res = driver.find_element_by_xpath('//div[@class="app-description__review-count"]').text
			find_rating = re.findall(r'\d+', res)
			user_count = int(''.join(find_rating))
			try:
				header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
				request = requests.get(url, headers=header)
				body = request.text
				soup = BeautifulSoup(body, 'html.parser')
				find_ratings = soup.find('script', {'type':'application/ld+json'}).get_text()
				load_ratings = json.loads(find_ratings)
				orig_score = float(load_ratings['aggregateRating']['ratingValue'])

				user_data = [user_rating, orig_score, user_count]
				data_to_update.append(user_data)

				print ("User Count = {}".format(user_count))
				print ("User Score = {}\n".format(orig_score))
				driver.quit()

			except AttributeError:
				driver.quit()
				print ('Empty data...\n')
			time.sleep(5)

		except NoSuchElementException:
			print ('No user yet...\n')
			driver.quit()

	except KeyboardInterrupt:
		print ('Stop...')
		driver.quit()
		break

print ('Done!!!')