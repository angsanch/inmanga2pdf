import inmanga
import requests
import img2pdf
import os

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