from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from settings import ROOT_FOLDER
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^esp/', include('esp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^$', 'libraro.pages.views.home'),
	(r'^robots.txt$', 'libraro.pages.views.robots'),
	(r'^read/$', 'libraro.pages.views.list_recent'),
	(r'^read/authors$', 'libraro.pages.views.list_authors'),
	(r'^contribute/$', 'libraro.pages.views.contribute'),
	(r'^read/(?P<person>\w*)/$', 'libraro.pages.views.person_profile'),
	(r'^read/(?P<author>\w*)/(?P<title>\w*).xml$', 'libraro.pages.views.xmlpage'),
	(r'^read/(?P<author>\w*)/(?P<title>\w*).html$', 'libraro.pages.views.htmlpage'),
	(r'^read/(?P<author>\w*)/(?P<title>\w*)/$', 'libraro.pages.views.page'),
	(r'^read/(?P<author>\w*)/(?P<title>\w*)/(?P<page>\w*)/$', 'libraro.pages.views.page'),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': ROOT_FOLDER+'/media/'}),
    (r'^admin/(.*)', admin.site.root),
)
