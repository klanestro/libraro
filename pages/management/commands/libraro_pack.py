import tarfile
from django.core.management.base import NoArgsCommand, CommandError
from libraro.settings import PROJECT_ROOT as root

class Command(NoArgsCommand):
    help = """
    Puts libraro.sqlite and the contents of media/works
    into an archive packed.tar. This archive can be pushed
    to github, unlike the database and the text files.
    packed.tar is overwritten.
    """

    def handle_noargs(self, **options):
        tar = tarfile.open(root + "/packed.tar", "w")
        tar.add(root + "/media/works","media/works")
        tar.add(root + "/libraro.sqlite","libraro.sqlite")
        tar.close()
