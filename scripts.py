#!/usr/bin/env python

import tarfile
import sys
import os

def pack():
	tar = tarfile.open("packed.tar", "w")
	tar.add("media/works")
	tar.add("esp.sqlite3")
	tar.close()

def unpack():
	tar = tarfile.open("packed.tar", "r")
	tar.extractall()

if __name__ == "__main__":
	if sys.argv[1] == "pack":
		pack()
	if sys.argv[1] == "unpack":
		unpack()
