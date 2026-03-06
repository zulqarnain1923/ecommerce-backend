from urllib import request

from user.models import User,Addtocart
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from api1.models.products import Products,Images
import re
# from api1.serializers import productserializer

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User

        fields='__all__'

    def validate(self,data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('this email is already exsist')
        return data
    def validate_password(self,password):
        if len(password) <8 :
            raise serializers.ValidationError('password must be of 8 characters')
        if not re.search(r'[a-z]',password):
            raise serializers.ValidationError('pssword must contain one lowercase latter')
    
        if not re.search(r'[A-Z]',password):
            raise serializers.ValidationError('pssword must contain one uppercase latter')

        if not re.search(r'[0-9]',password):
            raise serializers.ValidationError('pssword must contain one number')

        if not re.search(r'[@$!%*?&]',password):
            raise serializers.ValidationError('pssword must contain one special character')
        
        return password
    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class catagoryproductserializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    class Meta:
        model=Products
        fields=['pr_id','pr_name','image']
    def get_image(self,obj):
       request=self.context.get('request')
       image= obj.product_images.filter(product_id=obj).first()
       if image:
           return (request.build_absolute_uri(image.image.url))
       return None


class Addtocartserializer(serializers.ModelSerializer):
    pr_id=serializers.CharField(write_only=True)
    product=catagoryproductserializer(read_only=True,many=True)

    class Meta:
        model=Addtocart 
        fields=['user','pr_id','product']


    def create(self,validated_data):
        
        prd=validated_data.pop('pr_id')
        user=self.context['request'].user
        product=Products.objects.get(pr_id=prd)
        cart, _=Addtocart.objects.get_or_create(user=user)
        cart.product.add(product)
        cart.save()
        return cart
    
        
