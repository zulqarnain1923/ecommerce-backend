from django.db import models


class Catagory(models.Model):
    name=models.CharField(max_length=70)
    def __str__(self):
        return self.name

class Keyword(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Weight(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Products(models.Model):
    pr_id=models.CharField(max_length=60,unique=True,blank=True)
    pr_name=models.CharField(max_length=24)
    pr_desc=models.CharField(max_length=300 )
    pr_price=models.IntegerField()
    strick_price=models.IntegerField()
    brand=models.CharField(default='other',blank=True)
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    stock=models.IntegerField()
    keywords=models.ManyToManyField(Keyword,blank=True)
    colors=models.ManyToManyField(Color,blank=True)
    sizes=models.ManyToManyField(Size,blank=True)
    weights=models.ManyToManyField(Weight,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pr_id
    


class Images(models.Model):
    product_id=models.ForeignKey(Products,to_field='pr_id',related_name='product_images',on_delete=models.CASCADE)
    image=models.ImageField(upload_to="product_images/")

