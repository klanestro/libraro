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
	tar = tarfile.open(libraro + "/packed.tar", "w")
	tar.add(libraro + "/media/works","media/works")
	tar.add(libraro + "/libraro.sqlite","libraro.sqlite")
	tar.close()

def unpack():
	tar = tarfile.open(libraro + "/packed.tar", "r")
	tar.extractall(libraro)
	
def rebuild(work):
	work.splitter_version = 0
	work.generate()	

helpstring = """
The following commands are implemented:

./scripts.py pack
   Puts libraro.sqlite and the contents of media/works
   into an archive packed.tar. This archive can be pushed
   to github, unlike the database and the text files.
   packed.tar is overwritten.

./scripts.py unpack
   Unpacks packed.tar, overwriting everything.

./scripts.py rebuild [id]
   For the work with the given id, it deletes the cached
   pages and all converted files, leaving only the raw XML 
   files, then rebuilds everything. If id is omitted, it
   does this for every work.
"""

if __name__ == "__main__":

	# Default to help
	if len(sys.argv) == 1:
		sys.argv.append("help")
	
	if sys.argv[1] == "pack":
		pack()
	elif sys.argv[1] == "unpack":
		unpack()
	elif sys.argv[1] == "rebuild":
		from pages.models import Work
		if len(sys.argv) > 2:
			try:
				rebuild(Work.objects.get(id=int(sys.argv[2])))
			except:
				print sys.argv[2] + " not found"
		else:
			for work in Work.objects.all():
				rebuild(work)
	elif sys.argv[1] == "help":
		print helpstring
