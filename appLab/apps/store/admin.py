from django.contrib import admin
from .models import Categories, Materials
from import_export.resources import ModelResource
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin

# Inlines

class MaterialsInline(admin.TabularInline):
    model = Materials
    extra = 0


# Resources
class CategoriesResource(ModelResource):
    class Meta:
        model = Categories
        use_bulk = True
        batch_size = 500


class MaterialsResource(ModelResource):
    class Meta:
        model = Materials
        use_bulk = True
        batch_size = 500


@admin.register(Categories)
class CategoriesAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = CategoriesResource
    list_display = ['name']
    inlines = (MaterialsInline, )


@admin.register(Materials)
class MaterialsAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = MaterialsResource
    list_display = ['code', 'item', 'description', 'stock', 'enabled', 'details', 'category']
    search_fields = ('description', 'item')
 
