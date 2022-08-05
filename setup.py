import shutil
import os

appName = "inmanga2pdf"

def move (filename):
	if os.path.isfile (filename):
		shutil.copyfile (filename, os.path.join (appName, filename))
	elif os.path.isdir (filename):
		shutil.copytree (filename, os.path.join (appName, filename))


if os.path.exists (appName): shutil.rmtree (appName)

os.system (f"pyinstaller --noconfirm --onedir --console --name {appName} main.py")
shutil.move (os.path.join ("dist", appName), appName)
shutil.rmtree ("build")
shutil.rmtree ("dist")
os.remove (f"{appName}.spec")

move ("firefox.json")
move ("geckodriver.exe")
move ("Firefox")

shutil.make_archive (appName, "zip", base_dir = appName)