from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import json
from selenium import webdriver

"""
	crawl first the product by id from link and scraped data through gog api
"""

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0'
options = Options()
options.add_argument("--no-sandbox")
options.add_argument('user-agent={user_agent}')
options.add_argument("--headless")
path = '/usr/bin/chromedriver'

data_to_update = []
base_url = "https://www.gog.com/game/"
gog_game_links = ['gog', 'game', 'links']
for product_id in gog_game_links:
	try:
		try:
			driver = webdriver.Chrome(path, chrome_options=options)
			url = base_url + product_id
			print (url)
			driver.get(url)
			time.sleep(10)
			product = driver.find_element_by_xpath('//div[@class="layout ng-scope"]')
			product_id = product.get_attribute('card-product')
			api = "https://reviews.gog.com/v1/products/" + str(product_id) + "/averageRating?reviewer=verified_owner"
			driver.get(api)
			time.sleep(5)
			pre = driver.find_element_by_tag_name("pre").text
			data = json.loads(pre)
			print ('\n')

			orig_score = data['value']
			user_count = data['count']
			print ("game_rating = {}".format(user_rating))
			print ("user_count = {}".format(user_count))
			print (' ')

		except NoSuchElementException:
			print ('no user yet...\n')
			driver.quit()

	except KeyboardInterrupt:
		print ('stop process...')
		break
		driver.quit()
		print ('driver stop...')

print ("Done!!!")
