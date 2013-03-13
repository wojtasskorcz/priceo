from django.contrib import admin
from priceo.models import Product, Shop, ProductShop, Category

class ProductAdmin(admin.ModelAdmin):
    pass

class ShopAdmin(admin.ModelAdmin):
    pass

class ProductShopAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(ProductShop, ProductShopAdmin)
admin.site.register(Category, CategoryAdmin)