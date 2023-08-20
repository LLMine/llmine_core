from django.contrib import admin
from core.models import *
from datasources.models import *

# Register your models here.

admin.site.register(ContentPool)
admin.site.register(ExtracterPrompt)
admin.site.register(Datasource)
admin.site.register(InjestedTextContent)
