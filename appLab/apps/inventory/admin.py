from django.contrib import admin
from django.utils.html import format_html
from apps.store.models import Materials
from .models import GivesItems, GivesTotal
from .form import GivesForm
from datetime import datetime

class GivesItemsInline(admin.TabularInline):
    model = GivesItems
    extra = 1 

        
class GivesTotalAdmin(admin.ModelAdmin):
    form = GivesForm
    list_display = ['student', 'get_gives', 'date_out', 'date_back', 'is_give', 'is_back', 'get_status']
    filter_horizontal = ['items',]


    def get_gives(self, obj):
        return ""
        

    def get_status(self, obj):
        today=datetime.now()
        date_back = datetime.combine(obj.date_back, today.time())
        if not obj.is_give:
            return "No entregado"
        
        if obj.is_give and not obj.is_back:
            if date_back < today:
                return "Exedido"
            else:
                return "En tiempo"
        else: 
            return "Devuelto"
    

admin.site.register(GivesTotal, GivesTotalAdmin)
admin.site.register(GivesItems)



