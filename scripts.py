#!/usr/bin/env python

import tarfile
import sys
import os

# scripts.py file location
scripts = os.path.normpath(os.path.join(os.getcwd(), __file__))
# Libraro root dir
libraro = os.path.dirname(scripts)
# Allow to import models
sys.path.append(os.path.split(libraro)[0])
os.environ["DJANGO_SETTINGS_MODULE"] = "libraro.settings"

def pack():
	tar = tarfile.open("packed.tar", "w")
	tar.add("media/works")
	tar.add("esp.sqlite3")
	tar.close()

def unpack():
	tar = tarfile.open("packed.tar", "r")
	tar.extractall()
	
def rebuild():
	from pages.models import Work
	for work in Work.objects.all():
		work.splitter_version = 0
		work.generate()

if __name__ == "__main__":
	if sys.argv[1] == "pack":
		pack()
	if sys.argv[1] == "unpack":
		unpack()
	if sys.argv[1] == "rebuild":
		rebuild()
