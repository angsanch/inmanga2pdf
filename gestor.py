import inmanga
import requests
import img2pdf
import os
import time
import urlmatch
import json

def startAPI (timeout=10, headless=True):
	global inm 
	inm = inmanga.inmangaAPI (timeout=timeout, headless=headless)
def stopAPI ():
	inm.end ()

def download_chapter (manga_url, chapter, filename):
	inm.select_manga (manga_url, chapter)

	url_list = inm.get_chapter_image_urls ()
	img_list = []
	for i in range (len (url_list)):
		img_list.append (requests.get (url_list[i]).content)

	open (filename, "wb").write (img2pdf.convert(img_list))

def download_manga (manga_url, dir):
	inm.select_manga (manga_url)
	for i in inm.chapterTitleList:
		download_chapter (manga_url, i, os.path.join (dir, 	f"{inm.manga_name}-{i}.pdf"))

def get_manga_name (manga_url):
	inm.select_manga (manga_url)
	return inm.manga_name

def select_in_page (frequency=1):
	inm.go_to_inmanga ()
	while True:
		#Check if page is new and try to insert buttons if they are not inserted yet
		if not inm.is_marked ():
			if urlmatch.urlmatch ("https://inmanga.com/ver/manga/*/*/*", inm.driver.current_url):
				inm.insert_buttons ()
			inm.insert_page_marker ()

		#Check if any button has been pressed and act if it has
		status = inm.check_buttons ()
		if status != None: break

		#Control amount of tabs
		inmanga.max_tabs (inm.driver, 1)

		time.sleep (frequency)
	status=json.loads (status)
	inm.select_manga (inm.driver.current_url)

	data = {}
	data["mode"]=status["kind"]
	if status["kind"] == "chapter": data["chapter"] = inm.currentChapter
	data["url"]=inm.driver.current_url
	data["manga_name"] = inm.manga_name

	return data