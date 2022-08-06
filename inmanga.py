import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import selenium.webdriver.support.expected_conditions as EC
import os
import json

class inmangaAPI:
	def __init__ (self, timeout=10, headless=True):
		self.timeout = timeout
		self.options = selenium.webdriver.FirefoxOptions ()
		if headless: self.options.add_argument ("--headless")

		if os.path.exists ("firefox.json"):
			self.json = json.loads (open ("firefox.json", "r").readline ())
			self.driverpath = self.json["driverpath"]
			self.binarypath = FirefoxBinary (self.json["binarypath"])
			self.driver = selenium.webdriver.Firefox (executable_path=self.driverpath, options=self.options, firefox_binary=self.binarypath)
		else:
			self.driverpath = "geckodriver.exe"
			self.driver = selenium.webdriver.Firefox (executable_path=self.driverpath, options=self.options)
		self.driver.set_window_size (1200, 600)

	def select_manga (self, url, chapter = None):
		if len (url.split ("/"))==7:
			raise ImportWarning ("You have provided the general warning of the manga, the programs needs the link to one of the chapters")
		self.driver.get (url)
		WebDriverWait (self.driver, self.timeout).until (EC.presence_of_element_located ((By.CLASS_NAME, "select2-selection__arrow"))).click ()
		self.chapterList = self.driver.find_element (By.ID, "select2-ChapList-results").find_elements (By.CSS_SELECTOR, "*")
		self.chapterTitleList = [i.get_attribute ("innerHTML") for i in self.chapterList]
		if chapter != None:
			self.chapterList[self.chapterTitleList.index (chapter)].click ()
		
		self.manga_name = WebDriverWait (self.driver, self.timeout).until (EC.presence_of_element_located ((By.TAG_NAME, "strong"))).find_element (By.TAG_NAME, "a").get_attribute ("innerHTML")
		self.manga_name = self.manga_name [self.manga_name.rfind (">")+2:-21]

		max_tabs (self.driver, 1)

	def get_chapter_image_urls (self):
		self.pageList = WebDriverWait (self.driver, self.timeout).until (EC.presence_of_element_located ((By.ID, "PageList"))).find_elements (By.CSS_SELECTOR, "*")
		self.baseURL = self.driver.find_elements (By.TAG_NAME, "img")[1].get_attribute ("src")
		self.baseURL = self.baseURL[:self.baseURL.rfind("/")]
		self.baseURL = self.baseURL[:self.baseURL.rfind("/")]

		return [f"{self.baseURL}/{i.get_attribute ('innerHTML')}/{i.get_attribute ('value')}" for i in self.pageList]

def max_tabs (driver, max):
	if len (driver.window_handles) > max:
		old_tab = driver.current_window_handle
		driver.switch_to.window(driver.window_handles[max])
		driver.close ()
		driver.switch_to.window(old_tab)
