from django.contrib import admin
from .models import NormalShip, WasteShip, NormalImage, WasteImage
from django.utils.html import format_html


class NormalShipAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image_tag', 'name',
        # 'port', 'tons', 'types', 'code',
        # 'is_vpass', 'is_ais', 'is_vhf', 'is_ff', 'is_train',
        'img_cnt', 'register', 'regit_date', 'is_train',
    )
    search_fields = ['id', 'name']

    def image_tag(self, obj):
        if obj.main_img == '':
            img_path = 'http://127.0.0.1:8000/media/NoImage.jpg'
            return format_html('<img src="{}" height="150px;"width="150px;"/>'.format(img_path))
        return format_html('<img src="{}" height="150px;"width="150px;"/>'.format(obj.main_img.url))
    image_tag.short_description = 'Image'


class WastedShipAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image_tag', 'img_cnt', 'info', 'types', 'lat', 'lon', 'is_train',
        'regit_date', 'register'
    )
    search_fields = ['info', 'id']

    def image_tag(self, obj):
        if obj.main_img == '':
            img_path = 'http://127.0.0.1:8000/media/NoImage.jpg'
            return format_html('<img src="{}" height="150px;"width="150px;"/>'.format(img_path))
        return format_html('<img src="{}" height="200px;"width="200px;"/>'.format(obj.main_img.url))
    image_tag.short_description = 'Image'


class NormalImgAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image_tag', 'n_name', 'register', 'regit_date'
    )
    search_fields = ['n_name__id']

    def image_tag(self, obj):
        if obj.img is None:
            return ""
        return format_html('<img src="{}" height="200px;"width="200px;"/>'.format(obj.img.url))
    image_tag.short_description = 'Image'


class WasteImgAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image_tag', 'w_id', 'register', 'regit_date',
    )
    search_fields = ['w_id__id']

    def image_tag(self, obj):
        if obj.img is None:
            return ""
        return format_html('<img src="{}" height="200px;"width="200px;"/>'.format(obj.img.url))
    image_tag.short_description = 'Image'


admin.site.register(NormalShip, NormalShipAdmin)
admin.site.register(WasteShip, WastedShipAdmin)
admin.site.register(NormalImage, NormalImgAdmin)
admin.site.register(WasteImage, WasteImgAdmin)