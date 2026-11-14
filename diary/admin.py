from django.contrib import admin
from .models import Entry


admin.site.site_header = 'Дневник — панель управления'
admin.site.site_title = 'Дневник'
admin.site.index_title = 'Администрирование'

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    list_filter = ("user", "created_at")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
