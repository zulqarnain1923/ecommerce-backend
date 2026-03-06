from rest_framework import serializers
from order.models import Order
from api1.models.products import Products
from django.db import transaction


class orderserializer(serializers.ModelSerializer):
    pr_id=serializers.CharField(write_only=True)
    user=serializers.SerializerMethodField()
    status=serializers.CharField(read_only=True)
    class Meta:
        model=Order
        fields=['id','user','pr_id','full_name','city','address','street_address','total_amount','variant','quantity','phone','postal_code','payment_method','status']

    def get_user(self, obj):
        return obj.user.name 
    # def get_user(self,obj):
    #     return obj.status


    def validate(self,data):
        if len(data['full_name'])>150:
            raise serializers.ValidationError('name is required')
        required_field=['city','address','street_address','total_amount','quantity','variant','phone','postal_code']
        for field in required_field:
            if field not in data or not data[field]:
                raise serializers.ValidationError(f"field '{field}' is required")

        return data
    
    def create(self,validated_data):
        prd=validated_data.pop('pr_id')
        prd=Products.objects.get(pr_id=prd)
        request=self.context['request']
        user=request.user

        with transaction.atomic():
            order=Order.objects.create(user=user,product=prd,**validated_data)
            order.save()
            
        return order

        