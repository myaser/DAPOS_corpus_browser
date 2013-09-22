from scrapper import models
from django.contrib import admin


class CriterionAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Criterion, CriterionAdmin)
