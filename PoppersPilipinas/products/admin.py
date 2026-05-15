from django.contrib import admin
from django.utils.html import format_html
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('prodname', 'price', 'stock', 'image_preview')
    search_fields = ('prodname',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

admin.site.register(Product, ProductAdmin)
