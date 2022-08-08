import gestor
import tkinter
import tkinter.filedialog
import tkinter.messagebox

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
	answer = tkinter.messagebox.askyesnocancel ("Decide mode popup", "Do you have the link to the manga")
	if answer:
		gestor.startAPI ()
		command_line ()
	elif answer == False:
		tkinter.messagebox.showinfo ("Instructions", "Go to the chapter you want to download and press one of the buttons")
		gestor.startAPI (headless=False)
		gestor.select_in_page ()

	gestor.stopAPI ()
	input ("--ended--")