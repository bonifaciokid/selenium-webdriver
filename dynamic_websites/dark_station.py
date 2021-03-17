from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import time
import json

"""
	Scraped darkstation.com critic reviews with infinite scroll page.
	Every scroll made, we will check the current scroll height to the previous height.
	Process will stop if height become equal after scrolling.
"""

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0'
options = Options()
options.add_argument('user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
path = '/usr/bin/chromedriver'
url = 'https://www.darkstation.com/reviews'
driver = webdriver.Chrome(path, chrome_options=options)
driver.get(url)
time.sleep(10)

scroll_height = 1200
links = []
while True:
	try:
		get_links = driver.find_elements_by_xpath('//a[@class="Blog-header-content-link"]')
		time.sleep(5)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)
		current_offset_height = driver.execute_script("return document.body.offsetHeight;")
		print (current_offset_height)
		get_links = driver.find_elements_by_xpath('//a[@class="Blog-header-content-link"]')
		for link in get_links:
			link = link.get_attribute('href')
			if link not in links:
				links.append(link)
				print (link)

		if scroll_height == current_offset_height:
			break
		scroll_height = current_offset_height
	except KeyboardInterrupt:
		driver.quit()

#saved scraped links and we will use scrapy because it more faster that the selenium
with open('dark_station_links.json', 'w+') as link:
	json.dump(links, link, indent=4)

driver.quit()
print ('Done!!!')