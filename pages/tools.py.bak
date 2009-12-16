# -*- coding:utf-8 -*- 
import datetime
import re
from xml.etree import ElementTree
import sys
from xml.dom import pulldom
import pickle
from libraro.convert import Parser

def wrap_words(text):
	prog = re.compile(r"([^<>\w])([\w']+)([^<>\w])", re.UNICODE)
	def foo(m):
		return "%s<v>%s</v>%s" % (m.group(1), m.group(2), m.group(3))
	return prog.sub(foo, prog.sub(foo, " "+text+" "))[1:-1]

def urlify(text):
	url = re.compile(r'[^ \ \w]', re.UNICODE).sub('',text.lower())
	return re.sub(r'\ ','_',url)#.decode('utf-8')

def xify(text):
	text = text
	orig = 'ĉĝĥŝĵŭ'.decode('utf-8')
	rep = 'cghsju'
	for num, letter in enumerate(orig):
		text = text.replace(letter, rep[num]+'x')
	return text

class MyParser(Parser):
	def fix(self,node):
		pass
	def validate(self,node):
		if node.text:
			pass
		elif node.tag.upper() == node.tag:
			node.tag = node.tag.lower()
		if node.tag == "poem":
			for child in node:
				if child.tag == "p":
					child.tag = "stanza"
				elif child.tag == "center":
					child.tag = "title"
				if child.tag not in ["stanza", "title"]:
					raise Exception("Tag not allowed inside poem on line %d" % child.line)
		elif node.tag == "i": node.tag = "em"
		elif node.tag == "b": node.tag = "strong"


INLINE_TAGS = ["strong","em","br"]
SELF_CLOSING_TAGS = ["br","hr"]

class Page_Splitter:
	version = 76
	
	def __init__(self, work):
		self.work = work

	def run(self, one_page=False, wrap_words=True):
		self.page_size = 4500
		self.wrapwords = wrap_words
		self.one_page = one_page
		self.pages = []
		self.curpage = ""
		self.footnotes = []
		self.contents = []
		_nobr = False
		_h2 = False
		
		parser = MyParser()
		root = parser.parse(open(self.work.workdir()+"/raw.txt","r"))
		
		self.section(root,root_section=True)
		self.end_page()
		
		self.num_pages = len(self.pages)
		if not self.one_page and self.contents and self.num_pages >= 3:
		# Make a table of contents
			table = '<table class="contents">'
			for c in self.contents:
				table += '<tr><td><a href="%s%d/">' % (self.work.fullurl(), c[0]) 
				table += '%s</a></td><td style="text-align:right">%d' % (c[1], c[0])
				table += '</td></tr>'
			table += "</table>"
			self.pages[0] = table + self.pages[0]
		# Make a title for the first page
		title = '<div class="title"><h1>' + self.wrap_words(self.work.title()['eo']) + "</h1>"
		title += '<p class="author">' + self.work.author.full() + "</p>"
		if self.work.translator != None:
			title += '<p class="translator">Tradukis ' + self.work.translator.full() + "</p>"
		title += "</div>"
		self.pages[0] = title + self.pages[0]

	
	def section(self,section,root_section=False):
		if not root_section:
			title = self.inline(section["title"], True)
			# Add to table of contents
			self.contents.append((len(self.pages)+1,title))
			self.append("<h2>%s</h2>" % self.inline(section["title"]))
			if section["title2"]:
				self.append("<h4>%s</h4>" % self.inline(section["title2"]))
		for preface in section["prefaces"]:
			if preface["title"]:
				self.append("<h3>%s</h3>" % self.inline(preface["title"]))
			if preface["title2"]:
				self.append("<h4>%s</h4>" % self.inline(preface["title2"]))
			self.paragraph(preface)
			if preface["signed"]:
				self.append('<p class="signed">%s</p>' % self.inline(preface["signed"]))
		self.paragraph(section)
	
	def append(self,text):
		self.curpage += text
		return len(self.curpage) > self.page_size
	
	def inline(self,node,no_wrap=False):
		ret = ""
		for child in node:
			if child.text:
				if no_wrap:
					ret += child.text
				else:
					ret += self.wrap_words(child.text)
			elif child.tag in INLINE_TAGS:
				ret += self.wrap_in_tag(child.tag, self.inline(child))
			elif child.tag == "footnote":
				self.footnotes.append(self.inline(child))
				ret += "<sup>%d</sup>" % len(self.footnotes)
		return ret
	
	def paragraph(self,node):
		# At least one paragraph uner a title
		at_least_one = False
		for child in node:
			if child.tag == "section":
				self.section(child)
			elif child.tag == "p":
				self.append("<p>%s</p>" % self.inline(child))
			elif child.tag == "center":
				self.append('<p class="center">%s</p>' % self.inline(child))
			elif child.tag == "img":
				url = self.work.dir() + "/img/" + child["name"]
				if child["float"]:
					text = '<p><img src="%s" style="float:%s" alt=""/></p>' % (url, child["float"])
				else:
					caption = ""
					if child["caption"]:
							caption = "<br/>" + self.inline(child["caption"])
					text = '<p class="image"><img src="%s" alt=""/>%s</p>' % (url, caption)
				self.append(text)
			elif child.tag == "poem":
				self.poem(child)
			elif child.tag == "hr":
				self.append('<p class="hr">*&nbsp;*&nbsp;*</p>')
				
			if child.tag in ["p","center","img"] and not self.one_page and len(self.curpage) > self.page_size:
				self.end_page()
	
	def poem(self,node):
		self.append('<blockquote class="verse">')
		for child in node:
			if child.tag == "stanza":
				self.append('<p>%s</p>' % self.inline(child))
				# Transfer to next page if space is running out
				if not self.one_page and len(self.curpage) > self.page_size:
					self.append('</blockquote>')
					self.end_page()
					self.append('<blockquote class="verse">')
			elif child.tag == "title":
				self.append('<p class="center">%s</p>' % self.inline(child))
		self.append('</blockquote>')
		
	def end_page(self):
		if self.curpage.strip():
			# Add footnotes
			if self.footnotes:
				self.curpage += '<div id="footnotes">'
				for i, footnote in enumerate(self.footnotes):
					self.curpage += '<p><sup>%d</sup> %s</p>' % (i+1, footnote)
				self.curpage += '</div>'
			# Append the page
			self.pages.append(self.curpage)
			# Clear current page and footnotes
			self.curpage = ""
			self.footnotes = []
			print "Page %d, %d characters" % (len(self.pages), len(self.pages[-1]))
	
	def wrap_in_tag(self, tag, content):
		#print tag
		if tag in SELF_CLOSING_TAGS:
			return "<" + tag + "/>"
		else:
			return "<%s>%s</%s>" % (tag, content, tag)
		
	def wrap_words(self, text):
		if self.wrapwords:
			return wrap_words(text)
		else:
			return text
		
	def __iter__(self):
		return enumerate(self.pages)
	
def replace_dict(text,d):
	l1 = d.keys()
	l2 = d.values()
	for i in range(0,len(l1)):
		text = text.replace(l1[i],l2[i])
	return text
