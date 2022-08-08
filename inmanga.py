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

	def go_to_inmanga (self):
		self.driver.get ("https://inmanga.com/")
	
	def insert_buttons (self):
		for i in range (5):
			try:
				self.driver.execute_script(add_button_script)
				break
			except:
				pass
	def check_buttons (self):
		try:
			return self.driver.find_element (By.ID, "inmanga2pdfButonPress").get_attribute ("payload")
		except:
			return None

	def insert_page_marker (self):
		self.driver.execute_script ("elem=document.createElement ('meta');elem.setAttribute('id','inmanga2pdfMarked');document.getElementsByTagName('head')[0].appendChild(elem);")
	def is_marked (self):
		try:
			self.driver.find_element (By.ID, "inmanga2pdfMarked")
			found = True
		except:
			found = False
		return found

	def end (self):
		self.driver.quit ()

def max_tabs (driver, max):
	if len (driver.window_handles) > max:
		old_tab = driver.current_window_handle
		driver.switch_to.window(driver.window_handles[max])
		driver.close ()
		driver.switch_to.window(old_tab)

add_button_script = """
buttons=document.getElementsByClassName("pull-right")[1];
buttons.parentElement.appendChild(buttons.cloneNode(true));
buttons=buttons.parentElement.children[1];
button1=buttons.children[0];
button2=buttons.children[1];
clone=button1.children[0].cloneNode(true);
button1.children[0].remove();
button1.appendChild(clone);
button1.children[1].classList.remove('custom-btn-label-left');
button1.children[1].classList.add('custom-btn-label-right');
button1.children[1].children[0].classList.remove('fa-arrow-left');
button1.children[1].children[0].classList.add('fa-arrow-down');
button2.children[1].children[0].classList.remove('fa-arrow-right');
button2.children[1].children[0].classList.add('fa-arrow-down');
clone=button2.children[1].children[0].cloneNode(true);
button2.children[1].appendChild(clone);
button1.children[0].innerHTML='Chapter';
button2.children[0].innerHTML='Manga';
button1.setAttribute('onclick','but=document.getElementById("inmanga2pdfButton");but.setAttribute("payload","chapter");but.click();');
button2.setAttribute('onclick','but=document.getElementById("inmanga2pdfButton");but.setAttribute("payload","manga");but.click();');
button3=document.createElement('button');
button3.setAttribute('id','inmanga2pdfButton');
button3.setAttribute('onclick',`(function(kind){
    payload=document.createElement('meta');
    payload.setAttribute('id','inmanga2pdfButonPress');
    payload.setAttribute('payload','{"kind":"'+kind+'"}');
    document.getElementsByTagName('head')[0].appendChild(payload);
})(kind=this.getAttribute('payload'));`);
document.head.appendChild(button3);
"""