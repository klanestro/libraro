# -*- coding:utf-8 -*- 
import datetime
import re
from xml.etree import ElementTree
import sys
from xml.dom import pulldom

def wrap_words(text):
	prog = re.compile(r"([^<>\w])([\w']+)([^<>\w])", re.UNICODE)
	def foo(m):
		return "%s<v>%s</v>%s" % (m.group(1), m.group(2), m.group(3))
	return prog.sub(foo, " "+text+" ")

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

class Page_Splitter:
	version = 36
	pagesize = 2000
	untouched_tags = ['p','em']
	nobr_elements = ['p','stanza','center','footnote','h2']
	def __init__(self, work):
		input = work.text("xml",True)
		events = pulldom.parse(input)
		self.pages = []
		self.curpage = ""
		self.footnotes = []
		contents = []
		self._poem = False
		_nobr = False
		_footnote = False
		_h2 = False
		
		for event, node in events:
			
			text = ""
			# If this is a new page and a poem was
			# interrupted on the last page
			if self.curpage == "" and self._poem:
				text += '<blockquote class="verse">'
			
			if event == 'CHARACTERS':
				text += wrap_words(wrap_words(node.data))
				
			elif event == 'START_ELEMENT':
				
				if node.nodeName == "poem":
					self._poem = True
					text += '<blockquote class="verse">'
				elif node.nodeName == "stanza":
					text += '<p>'
				elif node.nodeName == "center":
					text += '<p class="center">'
				elif node.nodeName == "br":
					text += "<br/>"
				elif node.nodeName == "hr":
					text += '<p class="hr">*&nbsp;*&nbsp;*</p>'
				elif node.nodeName == "footnote":
					_footnote = True
					# The text will be added to the *last* footnote
					# so let's create a new one
					self.footnotes.append("")
					text += '<sup>%d</sup>' % len(self.footnotes)
				elif node.nodeName == "h2":
					_h2 = True
					contents.append([len(self.pages)+1,""])
					text += "<h2>"
					
				if node.nodeName in Page_Splitter.untouched_tags:
					text += '<%s>' % node.nodeName
					
				if node.nodeName in Page_Splitter.nobr_elements:
					_nobr = True
					
			elif event == 'END_ELEMENT':
				
				if node.nodeName == "poem":
					self._poem = False
					text += '</blockquote>'
				elif node.nodeName == "stanza":
					text += '</p>'
				elif node.nodeName == "center":
					text += '</p>'
				elif node.nodeName == "footnote":
					_footnote = False
				elif node.nodeName == "h2":
					_h2 = False
					text += "</h2>"
					
				if node.nodeName in Page_Splitter.untouched_tags:
					text += '</%s>' % node.nodeName 
				
				if node.nodeName in Page_Splitter.nobr_elements:
					_nobr = False
			
			if _footnote and node.nodeName != "footnote":
				self.footnotes[-1] += text	
			elif _h2  and node.nodeName != "h2":
				contents[-1][1] += text
				self.curpage += text
			else:
				self.curpage += text
				
			# Fires after </p> and if pagesize is enough
			if not _nobr and len(self.curpage) >= Page_Splitter.pagesize:
				self.endpage()
		
		if self.curpage:
			self.endpage()
			
		self.num_pages = len(self.pages)
		if contents:
		# Make a table of contents
			table = '<table class="contents">'
			for c in contents:
				table += '<tr><td><a href="%s%d">' % (work.fullurl(), c[0]) 
				table += '%s</a></td><td style="text-align:right">%d' % (c[1], c[0])
				table += '</td></tr>'
			table += "</table>"
			self.pages[0] = table + self.pages[0]
		# Make a title for the first page
		self.pages[0] = "<h1>" + wrap_words(work.title()['eo']) + "</h1>" + self.pages[0]
		
	def endpage(self):
		# Are we in the middle of a poem?
		if self._poem:
			self.curpage += '</blockquote>'
		# Were there any self.footnotes?
		if self.footnotes:
			self.curpage += '<div id="self.footnotes">'
			for i, footnote in enumerate(self.footnotes):
				self.curpage += '<p><sup>%d</sup>%s</p>' % (i+1, footnote)
			self.curpage += '</div>'
		# Append the page
		self.pages.append(self.curpage)
		# Clear
		self.curpage = ""
		print "Page %d" % (len(self.pages) + 1)
		
	def __iter__(self):
		return enumerate(self.pages)	

def replace_dict(text,d):
	l1 = d.keys()
	l2 = d.values()
	for i in range(0,len(l1)):
		text = text.replace(l1[i],l2[i])
	return text
