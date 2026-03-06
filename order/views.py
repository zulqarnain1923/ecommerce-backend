from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from order.serializer import orderserializer
from order.models import Order
from api1.models.products import Products
from user.models import User
from django.db import transaction 
from django.db.models import Sum ,Count
from django.db.models.functions import TruncMonth
from datetime import timedelta
from django.utils import timezone

# Create your views here.

class order(APIView):
    permission_classes=[IsAuthenticated]

    def post(slelf,request):
        data=request.data

        if request.method== 'POST':
            print(data)
            
            serializer=orderserializer(data=data,context={'request':request})
            if serializer.is_valid():
                with transaction.atomic():
                    serializer.save()
                    pr_id=data.get('pr_id')
                    quantity= int(data.get('quantity'))
                    prd=Products.objects.get(pr_id=pr_id)
                    prd.stock=prd.stock-quantity
                    prd.save()
                return Response(serializer.data,status=200) 
            return Response(serializer.errors)
        return  Response({'msg','error is occured'})
    
    def get(self,request):
        if request.user.is_staff:
            if request.method == 'GET':
                status=request.GET.get('status')
                data=Order.objects.select_related('user').filter(status=status.lower())
                serializer=orderserializer(data,many=True)
                return Response(serializer.data) 
        else:
            return Response({'msg':'wrong info'},status=403)
        
    def put(self, request):
        if request.user.is_staff:
            data=request.data
            print(data)
            order=Order.objects.get(id=data["id"])
            order.status=data['status'].lower()
            order.save()
            print(data)
            return Response({'msg':'data is submited'})
        else:
            return Response({'msg':'invalid user'},status=403)
        
@api_view(['GET'])
def monthlydata(request):

    five_months_ago = timezone.now() - timedelta(days=150)

    monthly_data = (
        Order.objects
        .filter(created_at__gte=five_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total_amount=Sum('total_amount'),
            total_orders=Count('id')
        )
        .order_by('month')
        )

    total_users = User.objects.count()
    total_products = Products.objects.count()
    total_orders = Order.objects.count()

    data = {
        "monthly_data": monthly_data,
        
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders
    }

    return Response(data)
