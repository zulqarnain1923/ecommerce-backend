



class productserializer(serializers.ModelSerializer):
  
    images = serializers.ListField(child=serializers.ImageField())
    keywords=serializers.ListField(child=serializers.CharField(),write_only=True)
    colors=serializers.ListField(child=serializers.CharField(),write_only=True,required=False)
    sizes=serializers.ListField(child=serializers.CharField(),write_only=True,required=False)
    weights=serializers.ListField(child=serializers.CharField(),write_only=True,required=False)
    
    
    class Meta:
        model = Products
        fields = [
            'pr_id', 'pr_name', 'pr_desc', 'strick_price', 'pr_price', 'keywords',
            'brand', 'catagory', 'stock', 'images','weights','colors','sizes'
        ]


    def to_representation(self, instance):

        representation= super().to_representation(instance)
        request=self.context.get('request')
        representation['colors']=[k.name for k in instance.colors.all()]
        representation['sizes']=[k.name for k in instance.sizes.all()]
        representation['weights']=[k.name for k in instance.weights.all()]
        # representation['keywords']=[k.name for k in instance.keywords.all()]

        if request is not None:
            representation['images'] = [request.build_absolute_uri(k.image.url) for k in instance.product_images.all() if k.image]
        else:
            representation['images'] = [k.image.url for k in instance.product_images.all() if k.image]
        return representation

# data validation

    def validate(self, data):

        for key, value in data.items():
            if isinstance(value, list) and key not in ['images', 'keywords','colors','sizes','weights']:
                if isinstance(value[0], str):
                    data[key] = value[0].lower()
                else:
                    data[key] = value[0]

        if len(data['pr_name']) > 24:
            raise serializers.ValidationError(
                'name max lenth is "24" character')
        if 'keywords' in data and (len(data['keywords']) > 6 or len(data['keywords']) < 1):
            raise serializers.ValidationError(
                'keyword length minimum "1" and maximum "6" ')
        if 'images' in data and (len(data['images']) > 6 or len(data['images'])<1):
            raise serializers.ValidationError(
                'image length minimum "1" and maximum "6" ')
        if 'colors' in data and len(data['colors']) > 6 :
            raise serializers.ValidationError('color length minimum "1" and maximum "6" ')
        if 'sizes' in data and len(data['sizes']) > 6 :
            raise serializers.ValidationError('size lenght minimum "1"and maximum "6" ')
        if 'weights' in data and len(data['weights']) > 6 :
            raise serializers.ValidationError('weitht lenght minimum "1" and maximum "6" ')
        return data

# create method
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        keyword = validated_data.pop('keywords', [])
        color= validated_data.pop('colors',[])
        size=validated_data.pop('sizes',[])
        weight=validated_data.pop('weights',[])
        
        name = validated_data.get('pr_name')
        catagory = validated_data.get('catagory')

# generate unique pr_id
        last_product = Products.objects.order_by('-id').first()
        if last_product:
            pr_id = f"{name}_{catagory.id}_{last_product.id + 1}"
        else:
            pr_id = f"{name}_{catagory.id}_1"
        print(pr_id)
        with transaction.atomic():

            prd = Products.objects.create(pr_id=pr_id, **validated_data)

            for k in keyword:
                kyw,_= Keyword.objects.get_or_create(name=k.strip().lower())
                prd.keywords.add(kyw)
            if len(color)>=1:
                for c in color:
                    cl,_=Color.objects.get_or_create( name=c.strip().lower())
                    prd.colors.add(cl)
            if len(size)>=1:
                for s in size:
                    sz,_=Size.objects.get_or_create( name=s.strip().lower())
                    prd.pr_sizes.add(sz)
            if len(weight)>=1:
                for weight in weight:
                    wg,_=Weight.objects.get_or_create(name=weight.strip().lower())
                    prd.pr_weights.add(wg)
            for img in images:
                Images.objects.create(product_id=prd, image=img)

        print('helow////////////////////////////////////////////////////////////////')
        return prd
