from rest_framework import serializers
from api1.models.products import Products, Catagory, Color, Size, Weight, Images, Keyword
from django.db import transaction


class catagoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = '__all__'


class keywordserializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'


class colorserializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']


class sizeserializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


class weightserializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ['id', 'name']

    
class productserializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    keywords = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    colors = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    sizes = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    weights = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Products
        fields = [
            'pr_id', 'pr_name', 'pr_desc',
            'strick_price', 'pr_price',
            'keywords', 'brand',
            'catagory', 'stock',
            'images', 'weights',
            'colors', 'sizes'
        ]

    def to_representation(self, instance):
        request = self.context.get('request')

        rep = super().to_representation(instance)

        rep['keywords'] = [k.name for k in instance.keywords.all()]
        rep['colors'] = [c.name for c in instance.colors.all()]
        rep['sizes'] = [s.name for s in instance.sizes.all()]
        rep['weights'] = [w.name for w in instance.weights.all()]

        if request:
            rep['images'] = [
                request.build_absolute_uri(img.image.url)
                for img in instance.product_images.all()
            ]
        else:
            rep['images'] = [
                img.image.url
                for img in instance.product_images.all()
            ]

        return rep

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        keywords = validated_data.pop('keywords', [])
        colors = validated_data.pop('colors', [])
        sizes = validated_data.pop('sizes', [])
        weights = validated_data.pop('weights', [])

        name = validated_data.get('pr_name')
        category = validated_data.get('catagory')

        last = Products.objects.order_by('-id').first()
        number = last.id + 1 if last else 1

        pr_id = f"{name}_{category.id}_{number}"

        with transaction.atomic():
            product = Products.objects.create(
                pr_id=pr_id,
                **validated_data
            )

            for k in keywords:
                obj, _ = Keyword.objects.get_or_create(name=k.strip().lower())
                product.keywords.add(obj)

            for c in colors:
                obj, _ = Color.objects.get_or_create(name=c.strip().lower())
                product.colors.add(obj)

            for s in sizes:
                obj, _ = Size.objects.get_or_create(name=s.strip().lower())
                product.sizes.add(obj)

            for w in weights:
                obj, _ = Weight.objects.get_or_create(name=w.strip().lower())
                product.weights.add(obj)

            for img in images:
                Images.objects.create(product_id=product, image=img)

        return product