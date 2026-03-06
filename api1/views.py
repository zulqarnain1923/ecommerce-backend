from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .models.products import Products, Catagory, Images
from api1.serializers import productserializer, catagoryserializer
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.


@api_view(['post', 'get', 'put', 'delete'])
def getdata(request, id=None):

    # full item get request
    if request.method == 'GET' and id:

        data = Products.objects.prefetch_related('sizes',
                                                 'colors',
                                                 'weights',
                                                 'product_images',
                                                 ).get(pr_id=id)
        serialize = productserializer(data, context={'request': request})
        return Response(serialize.data)

# dashboard product get request
    if request.method == 'GET' and id == None:
        products = Products.objects.all()
        stock = request.GET.get('stock')
        dashproduct = request.GET.get('dashproduct')
        minprice = request.GET.get('minprice')
        maxprice = request.GET.get('maxprice')
        catagory= request.GET.get('catagory')
        name=request.GET.get('name')
        print(name)
        data = []

# dashboard per prduct return
        if dashproduct:
            if stock == 'low stock':
                products = Products.objects.filter(stock__lte=10)
            if stock == 'in stock':
                products = Products.objects.filter(stock__gt=10)

            for p in products:
                data.append({
                    'pr_id': p.pr_id,
                    'pr_name': p.pr_name,
                    'stock': p.stock,
                    'pr_price': p.pr_price,
                })
            return Response(data)

# filter quer call 
        if minprice and maxprice:
            products=Products.objects.filter(Q(pr_price__lte=maxprice) & Q(pr_price__gte=minprice))
        if catagory :
            if catagory== 'All':
                pass
            else:
                prd=Catagory.objects.get(name=catagory)
                products=Products.objects.filter(catagory=prd.id)

# search by keyword and retrun data
        if name:
            query=Q()
            for i in name.split():
               query |=(Q(pr_desc__icontains=i)| Q(pr_name__icontains=i)|Q(keywords__name__icontains=i))
               
            products=Products.objects.filter(query).distinct()


# product data return request
        for p in products:
            image = []
            img = Images.objects.filter(product_id=p.pr_id)
            for i in img:
                image.append(request.build_absolute_uri(i.image.url))
            data.append({
                'pr_id': p.pr_id,
                'pr_name': p.pr_name,
                'pr_desc': p.pr_desc,
                'pr_price': p.pr_price,
                'strick_price': p.strick_price,
                'images': image
            })
        return JsonResponse(data, safe=False)


@api_view(['post'])
@parser_classes([MultiPartParser, FormParser])
def post(request):
    if request.method == 'POST':
        data = request.data.copy()
        print(data)
        serialize = productserializer(data=data)
        # return Response({'msg':'data is submitted'}, status=201)  # Return saved object
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=201)  # Return saved object
        else:
            print('serializer', serialize.errors)
            return Response(serialize.errors, status=400)


@api_view(['post', 'get', 'delete', 'put'])
# @parser_classes([MultiPartParser, FormParser])
def catagory(request, id=None):
    if request.method == 'GET' and id == None:
        data = Catagory.objects.all()
        serialize = catagoryserializer(data, many=True)
        return Response(serialize.data)

    if request.method == 'POST' and id:
        data = request.data
        serialize = catagoryserializer(data=data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=201)
        return Response(serialize.errors, status=400)
