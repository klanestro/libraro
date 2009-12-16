from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from libraro.pages.models import Work

def rebuild(work):
    work.splitter_version = 0
    work.generate()
    
class Command(BaseCommand):
    help = """
    For the work with the given id, it deletes the cached
    pages and all converted files, leaving only the raw XML 
    files, then rebuilds everything. If id is omitted, it
    does this for every work."""
    def handle(self, *args, **options):
        if args:
            try:
                rebuild(Work.objects.get(id=int(args[0])))
            except Work.DoesNotExist:
                print args[0] + " not found"
        else:
            for work in Work.objects.all():
                rebuild(work)
