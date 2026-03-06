from operator import add

from django.shortcuts import render
from rest_framework.decorators import APIView,api_view
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from .serializer import Userserializer,Addtocartserializer
from rest_framework.response import Response
from api1.models.products import Products
from user.models import Addtocart

# Create your views here.c



class checkuser(APIView):
    # permission_classes = [AllowAny]
    # authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        if request.user and request.user.is_authenticated:
            data=Products.objects.get(id=2)
            d={
                "pr_id":data.pr_id
            }
            return Response(d)
        else:
            return Response({'message':'user does not exist '},status=401)
        

# access token k liye view function 
@api_view(['POST'])
def token(request):
    data=request.data
    try:
        refresh=RefreshToken(data['refresh'])
        res={'access':str(refresh.access_token)}
        return Response(res)
    except :
        return Response({'msg':'token is not valid'},status=401)


# login user k liye views function
@api_view(['POST'])
def userlogin(requset):
    data=requset.data 
    print(data)
    if User.objects.filter(email=data['email']).exists:
        user=User.objects.get(email=data['email'])
        if user.check_password(data['password']):
            refresh=RefreshToken.for_user(user)
            res={
                'status':400,
                'refresh': str(refresh),
                'access' : str(refresh.access_token),
                'message': "user login successfully"
            }
            return Response(res)
        return Response({'msg':'wrong password'})
    return Response({'msg':'user not exists'})
    

# user register kliye view function    
@api_view(['POST'])
def userregister(request):
    data=request.data 
    serializer=Userserializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


# add to cart itme view function  
class Cartadded(APIView):
    permission_classes=[IsAuthenticated]
    # permission_classes=[AllowAny]
    # authentication_classes=[JWTAuthentication]
    def post(self,request):
        data=request.data 
        print(data)
        serializer=Addtocartserializer(data=data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
    
            return Response(['product added to cart successfully'])
        return Response(serializer.errors)
    
    def get(self,request):
        user=request.user
        flag=Addtocart.objects.filter(user=user).exists()
        # user=Addtocart.objects.filter(user=6).exists()
        if flag:
            cart=Addtocart.objects.get(user=user)
            
            serializer=Addtocartserializer(cart,context={'request':request})
            print(serializer.data)
            return Response(serializer.data)
        else:
            return Response({'msg':'your cart is empty'})
        
    def delete(self,request):
        data=request.data
        user=request.user
        prd=Products.objects.get(pr_id=data['pr_id'])
        cart=Addtocart.objects.get(user=user)
        cart.product.remove(prd)
        cart.save()
        return Response(['product removed from cart successfully'])
        
        
            
    

