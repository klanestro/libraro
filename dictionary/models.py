from django.db.models import *

class Definition(Model):
    en = TextField(primary_key=True)
    eo = TextField()

