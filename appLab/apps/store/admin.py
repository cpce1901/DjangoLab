from django.contrib import admin
from .models import Categories, Materials
# Register your models here.

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name']

class MaterialsAdmin(admin.ModelAdmin):
    list_display = ['category', 'code', 'item', 'description', 'stock', 'enabled']
 

admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Materials, MaterialsAdmin)