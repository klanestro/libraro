# -*- coding:utf-8 -*-
import re
import math
import time
import os
import shutil

from xml.etree import ElementTree

from django.db.models import *
from django.http import Http404

import tools
from tools import xify, urlify, Page_Splitter
from libraro.settings import MEDIA_ROOT as media

class Source(Model):
	url = CharField(max_length=200)
	name = CharField(max_length=200)
	def __unicode__(self):
		return self.name

class Type(Model):
	name = CharField(max_length=200)
	plural = CharField(max_length=200)
	def cap(self):
		return self.name[0].capitalize() + self.name[1:]
	def plural_cap(self):
		return self.plural[0].capitalize() + self.plural[1:]
	def __unicode__(self):
		return self.name

class Genre(Model):
	name = CharField(max_length=200)
	def __unicode__(self):
		return self.name


class Person(Model):
	first = CharField(max_length=30)
	last = CharField(max_length=30)
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	license = CharField(max_length=2000, blank=True, null=True)
	gender = CharField(max_length=1, choices=GENDER_CHOICES)
	url = CharField(max_length=60, editable=False)
	profile = TextField(blank=True, null=True)
	fileas = CharField(max_length=62, editable=False)
	born = IntegerField(blank=True, null=True)
	died = IntegerField(blank=True, null=True)
	def fullurl(self):
		return "/read/" + self.url
	def sex(self, m, f):
		if self.gender == "M": return m
		else: return f
	def him_her(self): return self.sex('him','her')
	def full(self):
		return self.first + " " + self.last
	def __unicode__(self):
		return self.fileas
	def save(self, force_insert=False, force_update=False):
		self.fileas = self.last + ', ' + self.first
		self.url = urlify(self.full())
		super(Person, self).save(force_insert, force_update)

class Work(Model):
	# Writing
	author = ForeignKey(Person, related_name="works")
	write_year = IntegerField(blank=True,null=True)
	write_license = CharField(blank=True,null=True,max_length=2000)
	# Translating
	translator = ForeignKey(Person, blank=True, null=True, related_name="translations")
	translation_year = IntegerField(blank=True, null=True)
	translation_license = CharField(blank=True,null=True,max_length=2000)
	# Titles and Languages
	titles = TextField(max_length=1000)
	title_languages = CharField(max_length=40)
	original_language = CharField(max_length=3, blank=True, null=True)
	# More stuff
	wtype = ForeignKey(Type, related_name="works", null=True, blank=True)
	genre = ForeignKey(Genre, related_name="works", null=True, blank=True)
	published = BooleanField(default=True)
	description = TextField(blank=True,null=True)
	source = ForeignKey(Source, related_name="works", null=True, blank=True)
	fulltext = TextField(blank=True, null=True)
	# Non-editable
	fileas = CharField(max_length=82, editable=False)
	url = CharField(max_length=60, editable=False)
	num_pages = IntegerField(editable=False, null=True)
	when_published = DateTimeField(editable=False, null=True)
	splitter_version = IntegerField(editable=False, null=True, default=0)
	
	def fullurl(self):
		return "/read/" + self.author.url + "/" + self.url
	
	def page(self,number):
		self.generate()
		if number > self.num_pages:
			raise Http404
		p = self.pages.all().get(number=number)
		return p.content

	def lang(self):
		l = {
		'ru':'Russian',
		'en':'English',
		'es':'Spanish',
		'da':'Danish'}
		if self.original_language == None:
			return None
		return l[self.original_language]

	def title(self):
		langs = self.title_languages.strip().split(',')
		titles = self.titles.strip().split('\n')
		if len(langs) != len(titles):
			raise Exception("Number of titles and title languages not equal")
		ret = dict(zip(langs,titles))
		if self.original_language != None:
			if self.original_language in langs:
				ret['original'] = ret[self.original_language]
		if not "en" in langs: # Fallback
			ret["en"] = ret["eo"]
		for i in ret.keys():
			ret[i] = ret[i].strip()
		return ret
	def origtitle(self):
		return self.title(self.original_language)
	
	def __unicode__(self):
		return self.fileas
		
	def link(self):
		return '<a href="#">Link to first page</a>'
	link.allow_tags = True
	
	def generate(self):
		# No need to generate
		if self.splitter_version == Page_Splitter.version:
			return
		# Delete all old pages
		self.pages.all().delete()

		splitter = Page_Splitter(self)
		splitter.run()
		
		self.num_pages = splitter.num_pages
		self.splitter_version = Page_Splitter.version

		super(Work, self).save(False, False)
		
		for num, page in splitter:
			Page(number=num+1, content=page, work=self).save()
		
		# Make new work.html
		new = open((media+"works/%d/work.html" % self.id), 'w')
		splitter.run(onepage=True,wrapwords=False)
		new.write(splitter.pages[0].encode('utf-8'))
		new.close()
		
	def save(self, force_insert=False, force_update=False):	
		title = self.title()['eo']
		self.url = urlify(title)
		# "Mysterious Island, The"
		if title.startswith('La '):
			self.fileas = title[3:] + ", La"
		else:
			self.fileas = title

		# If it is just published
		if self.published == True and self.when_published == None:
			self.when_published = datetime.datetime.utcnow()
		
		super(Work, self).save(force_insert, force_update)
		
		workdir = media+"works/%d" % self.id
		if not os.path.exists(workdir):
			os.mkdir(workdir)
		
		if self.fulltext != "" and self.fulltext != None:
			xml = open(workdir+"/work.xml","w")
			xml.write(self.fulltext.encode('utf-8'))
			xml.close()
			self.fulltext = ""
			self.generate()
	
	def text(self, format, as_file=False):
		workdir = media+"works/%d/" % self.id
		if format == "xml":
			f = "work.xml"
		elif format == "html":
			self.generate()
			f = "work.html"
		if as_file:
			return open(workdir + f, 'r')
		else:
			return open(workdir + f, 'r').read()

class Page(Model):
	number = IntegerField()
	content = CharField(max_length=5000)
	work = ForeignKey(Work, related_name="pages")
