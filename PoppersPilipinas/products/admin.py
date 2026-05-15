from django.contrib import admin
from django.utils.html import format_html
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('prodname', 'price', 'stock', 'image_preview')
    search_fields = ('prodname',)
    fields = ('prodname', 'price', 'description', 'stock', 'image_url')

    def image_preview(self, obj):
        image_src = None
        if obj.image:
            image_src = obj.image.url
        elif obj.image_url:
            image_src = obj.image_url

        if image_src:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', image_src)
        return "No Image"
    image_preview.short_description = 'Image Preview'

admin.site.register(Product, ProductAdmin)
