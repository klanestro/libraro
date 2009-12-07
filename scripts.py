#!/usr/bin/env python

import tarfile
import sys
import os
import re

# scripts.py file location
scripts = os.path.normpath(os.path.join(os.getcwd(), __file__))
# Libraro root dir
libraro = os.path.dirname(scripts)
# Allow to import models
sys.path.append(os.path.split(libraro)[0])
os.environ["DJANGO_SETTINGS_MODULE"] = "libraro.settings"

from libraro.settings import MEDIA_ROOT
from pages.models import Work

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

def clean(work):
	from pages.tools import MyParser
	from convert import converter
	"""
	filename = "%sworks/%d/work.xml" % (MEDIA_ROOT, work.id)
	clean = unescape(open(filename, "r").read().decode("utf-8"))
	clean = clean.replace("<i>", "<em>")
	clean = clean.replace("</i>", "</em>")
	clean = clean.replace("<b>", "<strong>")
	clean = clean.replace("</b>", "</strong>")
	clean = clean.replace("<BR>", "<br/>")
	clean = clean.replace("<HR>", "<hr/>")
	open(filename, "w").write(clean.encode("utf-8"))
	print "Cleaned XML %s" % filename
	conv = converter(
		xmlf = work.workdir() + "/work.xml",
		pyxf = work.workdir() + "/raw.txt"
	)
	conv.xml2pyx()
	"""
	print "Validating..."
	parser = MyParser()
	root = parser.parse(open(work.workdir()+"/raw.txt","r"))
	parser.output(work.workdir()+"/raw.txt")
	print "Valid or fixed. Try rebuilding"

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

./scripts.py clean [id]
	For the work with the given id, it performs standard cleaning 
	operations on the XML file, then converts it to PYX, then validates
	it. If id is omitted, it does this for every work.
"""

def unescape(text): # http://stackoverflow.com/users/62262/karlcow
	import htmlentitydefs
	"""Removes HTML or XML character references 
	and entities from a text string.
	@param text The HTML (or XML) source text.
	@return The plain text, as a Unicode string, if necessary.
	from Fredrik Lundh
	2008-01-03: input only unicode characters string.
	http://effbot.org/zone/re-sub.htm#unescape-html
	"""
	def fixup(m):
		text = m.group(0)
		if text[:2] == "&#":
		# character reference
			try:
				if text[:3] == "&#x":
					return unichr(int(text[3:-1], 16))
				else:
					return unichr(int(text[2:-1]))
			except ValueError:
				print "Value Error"
				pass
		else:
		# named entity
		# reescape the reserved characters.
			try:
				if text[1:-1] == "amp":
					text = "&amp;amp;"
				elif text[1:-1] == "gt":
					text = "&amp;gt;"
				elif text[1:-1] == "lt":
					text = "&amp;lt;"
				else:
					print text[1:-1]
					text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError:
				print "keyerror"
				pass
			return text # leave as is
	return re.sub("&#?\w+;", fixup, text)

if __name__ == "__main__":

	# Default to help
	if len(sys.argv) == 1:
		sys.argv.append("help")
	
	if sys.argv[1] == "pack":
		pack()
	elif sys.argv[1] == "unpack":
		unpack()
	elif sys.argv[1] == "rebuild":
		if len(sys.argv) > 2:
			try:
				rebuild(Work.objects.get(id=int(sys.argv[2])))
			except Work.DoesNotExist:
				print sys.argv[2] + " not found"
		else:
			for work in Work.objects.all():
				rebuild(work)
	elif sys.argv[1] == "help":
		print helpstring
	elif sys.argv[1] == "clean":
		if len(sys.argv) > 2:
			try:
				clean(Work.objects.get(id=int(sys.argv[2])))
			except Work.DoesNotExist:
				print sys.argv[2] + " not found"
		else:
			for work in Work.objects.all():
				clean(work)

			

