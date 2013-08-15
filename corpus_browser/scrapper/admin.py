from corpus_browser.scrapper import models
from django.contrib import admin


class HeursticAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Heurstic, HeursticAdmin)
