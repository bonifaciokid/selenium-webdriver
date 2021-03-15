from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import json
from selenium import webdriver

"""
	In this case, playstation new and upcoming link is a dynamic page so I used Selenium. Scrapy is fast, so all crawled links will be used by it.
"""

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0'
options = Options()
options.add_argument("--no-sandbox")
options.add_argument('user-agent={user_agent}')
options.add_argument("--headless")
path = '/usr/bin/chromedriver'

urls = ['https://store.playstation.com/en-us/category/a00d4d61-f6bc-4a00-bb68-ff0bb43fcc33/1', 'https://store.playstation.com/en-us/category/a00d4d61-f6bc-4a00-bb68-ff0bb43fcc33/2']
driver = webdriver.Chrome(path, chrome_options=options)
game_links = []
for url in urls:
	driver.get(url)
	time.sleep(10)
	links = driver.find_elements_by_xpath('//a[@class="ems-sdk-product-tile-link"]')
	for link in links:
		game_link = link.get_attribute('href')
		print (game_link)
		game_link.append(game_link)

with open('ps_new_games.json', 'w+') as new:
	json.dump(game_links, new, indent=4)

driver.quit()
