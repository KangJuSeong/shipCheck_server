from django.contrib import admin
from .models import Boat, WasteBoat
from django.utils.html import format_html


class BoatAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'imo', 'calsign', 'mmsi', 'vessel_type', 'build_year',
        'current_flag', 'home_port', 'image_tag'
    )

    def image_tag(self, obj):
        return format_html('<img src="{}" height="150px;"width="150px;"/>'.format(obj.main_img.url))
    image_tag.short_description = 'Image'


admin.site.register(Boat, BoatAdmin)
admin.site.register(WasteBoat)