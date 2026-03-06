from django.contrib import admin
from order.models import Order
# Register your models here.


@admin.register(Order)
class orderadmin(admin.ModelAdmin):
    list_display=['full_name','total_amount','status']
