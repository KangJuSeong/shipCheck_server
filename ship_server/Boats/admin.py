from django.contrib import admin
from .models import Boat, WasteBoat


class BoatAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'reserve', 'product_status', 'manufacturer', 'brand',
        'model_code', 'thumbnail_preview'
    )

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

admin.site.register(Boat, BoatAdmin)
admin.site.register(WasteBoat)