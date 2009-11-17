# -*- coding: utf-8 -*-


roots = open('/home/boroninh/libraro/roots.txt','r').read().decode('utf-8').strip().split("\n")	
prefixes=[u"ali",u"bo",u"dis",u"ek",u"eks",u"fi",u"ge",u"i",u"ki",u"mal",u"neni",u"pra",u"re",u"ti",u"ĉef",u"ĉi",u"ne"]
suffixes=set([u"aĵ",u"ar",u"ant",u"ad",u"at",u"aĉ",u"ant",u"an",u"ar",u"ec",u"eg",u"estr",u"et",u"ej",u"ebl",u"em",u"er",u"ent",u"el",u"ec",u"end",u"ig",u"iĝ",u"ing",u"int",u"ist",u"in",u"iĉ",u"ind",u"in",u"il",u"id",u"ism",u"it",u"int",u"obl",u"ont",u"op",u"ot",u"on",u"ont",u"uj",u"ul",u"um",u"ut",u"unt",u"ĉj"])
v_ends = ['as','is','os','us','u']

morphemes = {"pre":set(), "root":set(), "suf":set()}

class Node:
	def __init__(self, type, body, rest, parent):
		self.parent = parent
		self.type = type
		self.body = body
		self.children = []
		self.rest = rest
		if rest != "":
			self.search()
		elif self.type == "end":
			self.define()
	def define(self):
		global morphemes
		if self.body == "": return
		if self.type in ["pre","root","suf"]:
			morphemes[self.type].add(self.body)
		self.parent.define()
	def search(self):
		# If it reached the end of the word
		if self.rest in ["o","e","a","i"]:
			self.addchild('end',self.rest)
			return
		ps = starts_with(self.rest, prefixes)
		rs = starts_with(self.rest, roots)
		ss = starts_with(self.rest, suffixes)
		if self.type in ["pre","suf","end"]:
			for m in ps:
				self.addchild("pre",m)
		if self.type in ["pre","root","suf","end"]:
			for m in rs:
				self.addchild("root",m)
		if self.type in ["root","suf"]:
			for m in ["o","a","e"]:
				if self.rest.startswith(m):
					self.addchild("end",m)
			for m in ss:
				self.addchild("suf",m)
	def addchild(self, type, body):
		self.children.append(Node(type,body,self.rest[len(body):],self))

def look(w):
	import sqlite3
	conn = sqlite3.connect('/home/boroninh/libraro/words.sqlite')
	cursor = conn.cursor()
	cursor.execute("select * from words where eo like ?", (w,))
	result = cursor.fetchone()
	conn.close()
	if result == None and w.endswith('o'):
		return look(w[:-1]+"a")
	if result == None and w.endswith('a'):
		return look(w[:-1]+"e")
	if result == None: return None
	return [w, result[0]]

def starts_with(word, keys):
	"""
	Returns only the keys that the word starts with
	"""
	return filter(lambda x: word.startswith(x), keys)

def doword(word):
	global morphemes
	morphemes = {"pre":set(), "root":set(), "suf":set()}
	# These roots will be ignored, because 99% of the time they
	# are really suffixes or prefixes
	ignore_roots = set(["il","ul","mal","ek"])
	
	defs = [look(word)]
	
	if defs == [None]:
		word = word.lower()	
		if word.endswith('n'):
			word = word[:-1]
		if word.endswith('j'):
			word = word[:-1]
		for end in ['as','is','os','us','u']:
			if word.endswith(end):
				word = word[:-len(end)]+"i"
		defs = [look(word)]
	
	if defs == [None]:
		word = Node("pre","",word,None)
		for m in morphemes["pre"]:
			defs.append(look(m+"-"))
		for m in morphemes["root"]:
			if m not in ignore_roots:
				defs.append(look(m+"o"))
		for m in morphemes["suf"]:
			defs.append(look("-"+m))
	defs = filter(lambda x: x != None, defs)	
	text = ""
	if defs:
		for d in defs:
			definition = ", ".join(d[1].split("|"))
			text += "<b>%s</b>: %s<br/>" % (d[0], definition)
		text = text[:-5]
	else:
		text = "Sorry, not found."

	return text
