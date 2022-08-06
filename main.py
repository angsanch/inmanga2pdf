import gestor
import tkinter
import tkinter.filedialog

root = tkinter.Tk () 
root.withdraw ()
root.attributes ('-topmost', True)

def command_line ():
	ans = input ("Download just one episode(1) or full manga(2): ")
	if ans == "1":
		manga_url = input ("Manga URL: ")
		chapter = input ("Chapter name: ")
		filename = tkinter.filedialog.asksaveasfilename (initialfile=f"Chapter {chapter}.pdf", filetypes=[("PDF file", "*.pdf")], title="Select where to save the episode")
		gestor.download_chapter (manga_url, chapter, filename)
	elif ans == "2":
		manga_url = input ("Manga URL: ")
		dir = tkinter.filedialog.askdirectory (title="Select the folder where all the manga will be stored")
		gestor.download_manga (manga_url, dir)


if __name__ == "__main__":
	gestor.startAPI ()
	command_line ()
	input ("--ended--")