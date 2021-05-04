from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources


# Register your models here.
class MealResource(resources.ModelResource):
    class Meta:
        model = Meal


class MealAdmin(ImportExportModelAdmin):
    resource_class = MealResource


admin.site.register(User)
admin.site.register(Meal, MealAdmin)
admin.site.register(UserReaction)
admin.site.register(News)
