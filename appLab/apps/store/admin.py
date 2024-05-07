from django.contrib import admin
from .models import Categories, Materials, Items, Gives
from .forms import GivesAdminForm, ItemsForm
from import_export.resources import ModelResource
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin


# INLINES
class ItemsInlines(admin.TabularInline):
    autocomplete_fields = ('item', )
    model = Items
    extra = 0
    form = ItemsForm

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('show_category', 'code', 'item','description', 'stock')
    ordering = ('id', )
    search_fields = ('description', 'code', 'item')
    list_filter = ('category', )

    @admin.display(description='categoria')
    def show_category(self, obj):
        return obj.category


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gives', 'item', 'count', 'is_back')



@admin.register(Gives)
class GivesAdmin(admin.ModelAdmin):
    list_display = ('date_out', 'student', 'date_back', 'show_status')
    autocomplete_fields = ('student', )
    inlines = [ItemsInlines, ]
    search_fields = ('student__name', 'student__email')
    form = GivesAdminForm

    @admin.display(description="status")
    def show_status(self, obj):
        all_items = obj.items_gives_gives.all()
        all_status = [not item.is_back for item in all_items]
        return 'pendiente' if any(all_status) else 'regresado'
