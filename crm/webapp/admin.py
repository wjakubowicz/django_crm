from django.contrib import admin
from . models import Record
from import_export.admin import ImportExportModelAdmin

admin.site.register(Record, ImportExportModelAdmin)
