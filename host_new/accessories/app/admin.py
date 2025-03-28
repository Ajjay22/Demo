from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([register,d_register,Order])
admin.site.register(add_product)
admin.site.register(Cart)