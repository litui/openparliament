from django.contrib import admin

from parliament.hansards.models import *

class DocumentOptions(admin.ModelAdmin):
    list_display=('number', 'date', 'session', 'document_type', 'committeemeeting')
    list_filter=('document_type', 'session', 'date', 'multilingual', 'public')

class StatementOptions(admin.ModelAdmin):
    list_display = ('politician', 'time', 'document', 'wordcount', 'procedural')
    #list_filter = ('time', 'procedural')
    raw_id_fields = ('document', 'member', 'politician', 'bills', 'mentioned_politicians')
    #ordering = ('-time',)
    
admin.site.register(Document, DocumentOptions)
admin.site.register(Statement, StatementOptions)