import tarfile
from django.core.management.base import CommandError, NoArgsCommand
from libraro.settings import PROJECT_ROOT as root

class Command(NoArgsCommand):
    help = """
    Unpacks packed.tar, overwriting everything.
    """
    def handle_noargs(self, **options):
        tar = tarfile.open(root + "/packed.tar", "r")
        tar.extractall(root)

