from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from settings import PROJECT_ROOT
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'libraro.pages.views.home'),
	(r'^robots.txt$', 'libraro.pages.views.robots'),
	(r'^read/$', 'libraro.pages.views.list_recent'),
	(r'^read/authors$', 'libraro.pages.views.list_authors'),
	(r'^contribute/$', 'libraro.pages.views.contribute'),
	(r'^read/(?P<person>\w*)/$', 'libraro.pages.views.person_profile'),
	(r'^read/(?P<author>\w*)/(?P<title>\w*)/print.html$', 'libraro.pages.views.htmlpage'),
	(r'^read/(?P<author>\w*)/(?P<title>\w*)/$', 'libraro.pages.views.page'),
	(r'^read/(?P<author>\w*)/(?P<title>\w*)/(?P<page>\w*)/$', 'libraro.pages.views.page'),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROJECT_ROOT+'/media/'}),
    (r'^admin/(.*)', admin.site.root),
)
