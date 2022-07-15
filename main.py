import gestor

def command_line ():
	ans = input ("Download just one episode(1) or full manga(2): ")
	if ans == "1":
		manga_url = input ("Manga URL: ")
		chapter = input ("Chapter name: ")
		dirpath = input ("In what folder do you want to store the pdf?: ")
		filename = input ("File name:") + ".pdf"
		gestor.download_chapter (manga_url, chapter, dirpath, filename)
	elif ans == "2":
		manga_url = input ("Manga URL: ")
		parentdir = input ("In what folder do you want to store the pdf?: ")
		dir = input ("File name:")
		gestor.download_manga (manga_url, parentdir, dir)


if __name__ == "__main__":
	command_line ()
	input ("--ended--")