from django.contrib import admin
from .models.products import Products,Images,Catagory,Color,Size,Weight,Keyword
# Register your models here.

@admin.register(Products)
class productAdmin(admin.ModelAdmin):
    list_display=['id','pr_id','pr_name','pr_desc','strick_price','pr_price','brand','catagory','stock','created_at','updated_at']

@admin.register(Catagory)
class productAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(Keyword)
class productAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(Color)
class productAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(Size)
class productAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(Weight)
class productAdmin(admin.ModelAdmin):
    list_display=['id','name']



@admin.register(Images)
class productAdmin(admin.ModelAdmin):
    list_display=['id','product_id','image']

# @admin.register(Colors)
# class productAdmin(admin.ModelAdmin):
#     list_display=['id','product_id','color']

# @admin.register(Sizes)
# class productAdmin(admin.ModelAdmin):
#     list_display=['id','product_id','size']

# @admin.register(Weights)
# class productAdmin(admin.ModelAdmin):
#     list_display=['id','product_id','weight']