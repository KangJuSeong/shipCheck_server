from django.contrib import admin
from .models import Boat, WasteBoat
from django.utils.html import format_html


class BoatAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image_tag', 'name', 'imo', 'calsign', 'mmsi', 'vessel_type', 'build_year',
        'current_flag', 'home_port', 'is_learning'
    )

    def image_tag(self, obj):
        if obj.main_img is None:
            return ""
        return format_html('<img src="{}" height="200px;"width="200px;"/>'.format(obj.main_img.url))
    image_tag.short_description = 'Image'


class WastedBoatAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'image_tag', 'detail', 'latitude', 'longitude', 'is_learning'
    )

    def image_tag(self, obj):
        if obj.wasted_img is None:
            return ""
        return format_html('<img src="{}" height="200px;"width="200px;"/>'.format(obj.wasted_img.url))
    image_tag.short_description = 'Image'


admin.site.register(Boat, BoatAdmin)
admin.site.register(WasteBoat, WastedBoatAdmin)