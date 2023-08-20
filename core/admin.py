from django.contrib import admin
from core.models import *
from datasources.models import *

# Register your models here.

admin.site.register(ContentPool)
admin.site.register(InjestedTextContent)
admin.site.register(ExtracterChain)
admin.site.register(ExtracterPrompt)
admin.site.register(ProcessedData)
admin.site.register(Datasource)
