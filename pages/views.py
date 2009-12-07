# -*- coding: utf-8 -*-

import re
import datetime

from libraro.settings import MEDIA_ROOT as media
from libraro.pages.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.files import File
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, Template
from tools import xify

def contribute(request):
	return render_to_response("contribute.html", {"active_tab":"contribute","additions": latest()})

def list_recent(request):
	temp = get_template('item.html')
	l = Work.objects.filter(published=True).order_by('-when_published')
	li = '<p>Showing newest to oldest. <a href="/read/authors">List authors alphabetically?</a></p><hr/>'
	for work in l:
		li += temp.render(Context({"work":work}))
	return render_to_response("base.html", {
	"title": "Recent Additions",
	"active_tab":"read",
	"content":li,
	"additions": latest()})

def list_authors(request):
	people = Person.objects.order_by('fileas')
	temp = get_template('author.html')
	li = '<p>Listing authors alphabetically. <a href="/read">Show latest additions?</a></p><hr/>'
	for person in people:
		if person.works.count() + person.translations.count() != 0:
			li += '<h1><a href="/read/'+person.url+'">' + person.full() + "</a></h1>"
			li += temp.render(Context({"person":person}))
	return render_to_response("base.html", {
	"title":"List of Authors",
	"active_tab":"read",
	"content":li,
	"additions": latest()})

def person_profile(request, person):
	person = get_object_or_404(Person, url=person)
	temp = get_template('author.html')
	worklist = temp.render(Context({"person":person}))
	
	return render_to_response("author_profile.html", {
	"worklist":worklist,
	"active_tab":"read",
	"person":person,
	"additions": latest()})

def home(request):
	return render_to_response("home.html", {"active_tab":"home", "additions": latest()})

def xmlpage(request, author, title):
	work = get_object_or_404(Work, url=title)
	response = HttpResponse(work.text("xml"), mimetype='application/xml')
	response['Content-Disposition'] = 'attachment; filename='+xify(work.url)+'.xml'
	return response

def htmlpage(request, author, title):
	work = get_object_or_404(Work, url=title)
	return render_to_response("htmlpage.html", {
	"content":work.text("html"),
	"work":work,
	"style":open(media+"page.css").read(),
	})

def page(request, author, title, page=1):
	page = int(page)
	size = 2000
	work = get_object_or_404(Work, url=title)	
	content = work.page(page)

	author = work.author
	translator = work.translator
	moreworks = author.works.exclude(id=work.id).filter(published=True)

	# Previous and next pages; -1 if it doesn't exist
	prev = page - 1
	if prev == 0: prev = -1
	next = page + 1
	if next == work.num_pages+1: next = -1
	
	# Figure out licenses
	now = datetime.datetime.utcnow().year - 1
	# Why minus 1? Because, if someone writes a work on April 2, 1937
	# it becomes public domain only in JANUARY 1, 2008
	wdelta, tdelta = -1, -1
	if author.died != None:
		adied = author.died
		wdelta = now - adied
			
	wlicense, tlicense = "", ""
	if wdelta >= 100:
		wlicense += "<p>The original work is in the public domain " \
		"worldwide because %s died more than 100 years ago.</p>" % author.full()
	elif wdelta >= 50:
		wlicense += "<p>%s died in %d, so %s works are in the public " \
		"domain in countries and areas where the copyright term is " \
		"the author&#8217;s life plus %d years or less." \
		"</p>" % (author.full(), adied, author.sex("his","her"), wdelta)
	if wdelta < 100:
		if work.write_license != None and work.write_license != "": 
			wlicense += work.write_license
		elif author.license != None:
			wlicense += author.license
	if wlicense == "":
		wlicense = "The original work&#8217;s license is uncertain."
	if translator != None:
		if translator.died != None:
			tdied = work.translator.died
			tdelta = now - tdied
			if tdelta >= 100:
				tlicense += "<p>The translation is in the public domain " \
				"worldwide because %s died more than 100 years ago.</p>" % translator.full()
			elif tdelta >= 50:
				tlicense += "<p>%s died in %d, so %s works are in the public " \
				"domain in countries and areas where the copyright term is " \
				"the author&#8217;s life plus %d years or less." \
				"</p>" % (translator.full(), tdied, translator.sex("his","her"), tdelta)
			if tdelta < 100:
				if work.translation_license != None: 
					wlicense += work.translation_license
				elif translator.license != None:
					wlicense += translator.license
		if tlicense == "":
			tlicense = "The translation license is uncertain."
	
	onepage = False
	if work.num_pages == 1: onepage = True
	
	return render_to_response("page.html", {
	"onepage": onepage,
	"license": wlicense + tlicense,
	"id": id,
	"page": page, 
	"content": content,
	"prev": prev,
	"next": next,
	"author": author,
	"work": work,
	"moreworks": moreworks,
	"active_tab": "read",
	"additions": latest()})

def latest():
	#filter(published=True)
	return Work.objects.filter(published=True).order_by('-when_published')[:7]

def robots(request):
	text = """User-agent: *
Allow: /
Disallow: /read/*.html$ """
	return HttpResponse(text, mimetype="text/plain")
