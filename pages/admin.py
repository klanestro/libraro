from libraro.pages.models import *
from django.contrib import admin

def resave(modeladmin, request, queryset):
	for a in queryset:
		a.save()
resave.short_description = "Resave"

class WorkAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Author", {
            'fields': ('author', 'write_year', 'write_license')
        }),
        ('Translator', {
            'classes': ('collapse',),
            'fields': ('translator', 'translation_year', 'translation_license')
        }),
        ("Work", {
            'fields': ('titles','title_languages','original_language', 'description', 'published', 'wtype', 'genre', 'source','fulltext')
        }),
    )
    actions = [resave]

admin.site.register(Person)
admin.site.register(Work, WorkAdmin)
admin.site.register(Source)
admin.site.register(Type)
admin.site.register(Genre)
#admin.site.register(Page)
