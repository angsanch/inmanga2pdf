import inmanga
import requests
import img2pdf
import os

inm = inmanga.inmangaAPI ()

def download_chapter (manga_url, chapter, dirpath = "", filename = None):
	inm.select_manga (manga_url, chapter)

	if filename == None: filename = f"{inm.manga_name}-{chapter}.pdf"

	url_list = inm.get_chapter_image_urls ()
	img_list = []
	for i in range (len (url_list)):
		img_list.append (requests.get (url_list[i]).content)

	open (os.path.join (dirpath, filename), "wb").write (img2pdf.convert(img_list))

def download_manga (manga_url, parentdir = "", dir = None):
	inm.select_manga (manga_url)
	if dir == None: dir = inm.manga_name
	path = os.path.join (parentdir, dir)
	if not os.path.exists (path): os.mkdir (path)

	for i in inm.chapterTitleList:
		download_chapter (manga_url, i, path)