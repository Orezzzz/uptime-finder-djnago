from django.contrib import admin
from .models import urlslist, urlshistory, deletedurls

# Register your models here.
class  urlshistoryamin(admin.ModelAdmin):
    list_display = ('urlslist', 'created_at', 'updated_at', 'status')


admin.site.register(urlshistory, urlshistoryamin)
admin.site.register(urlslist)
admin.site.register(deletedurls)