from django.contrib import admin
from .models import *


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(FlashSale)
admin.site.register(ProductViewHistory)

