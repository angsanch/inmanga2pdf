import gestor
import tkinter
import tkinter.filedialog
import tkinter.messagebox

root = tkinter.Tk () 
root.withdraw ()
root.attributes ('-topmost', True)

def command_line (data={}):
	keys = data.keys()
	def get_from_data (key, ifnot):
		if key not in keys: return ifnot ()
		else: return data[key]
	
	ans = get_from_data ("mode", lambda: input ("Download just one episode(1) or full manga(2): "))
	if ans == "1":
		manga_url = get_from_data ("url", lambda: input ("Manga URL: "))
		chapter = get_from_data ("chapter", lambda: input ("Chapter name: "))
		filename = get_from_data ("path", lambda: tkinter.filedialog.asksaveasfilename (initialfile=f"{gestor.get_manga_name (manga_url)}-{chapter}.pdf", filetypes=[("PDF file", "*.pdf")], title="Select where to save the episode"))
		gestor.download_chapter (manga_url, chapter, filename)
	elif ans == "2":
		manga_url = get_from_data ("url", lambda: input ("Manga URL: "))
		dir = get_from_data ("path", lambda: tkinter.filedialog.askdirectory (title="Select the folder where all the manga will be stored"))
		gestor.download_manga (manga_url, dir)


if __name__ == "__main__":
	answer = tkinter.messagebox.askyesnocancel ("Decide mode popup", "Do you have the link to the manga")
	if answer:
		gestor.startAPI ()
		command_line ()
	elif answer == False:
		tkinter.messagebox.showinfo ("Instructions", "Go to the chapter you want to download and press one of the buttons")
		gestor.startAPI (headless=False)
		data = gestor.select_in_page ()
		if data["mode"] == "chapter": data["mode"] = "1"
		elif data["mode"] == "manga": data["mode"] = "2"
		gestor.stopAPI ()
		gestor.startAPI ()
		command_line (data)

	gestor.stopAPI ()
	input ("--ended--")