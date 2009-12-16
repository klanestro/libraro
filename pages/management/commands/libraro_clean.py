from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from libraro.pages.models import Work

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
    print 'Validating "%s" (%d)' % (work.title()['eo'], work.id)
    parser = MyParser()
    root = parser.parse(open(work.workdir()+"/raw.txt","r"))
    parser.output(work.workdir()+"/raw.txt")
    print "Valid or fixed. Try rebuilding"
    
class Command(BaseCommand):
    help = """
    For the work with the given id, it performs standard cleaning 
    operations on the XML file, then converts it to PYX, then validates
    it. If id is omitted, it does this for every work."""
    def handle(self, *args, **options):
        if args:
            try:
                clean(Work.objects.get(id=int(args[0])))
            except Work.DoesNotExist:
                print args[0] + " not found"
        else:
            for work in Work.objects.all():
                clean(work)

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
