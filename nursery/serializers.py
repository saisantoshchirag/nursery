from .models import Plants,Order,Nursery
from rest_framework import serializers

class NurserySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nursery
        fields = "__all__"

class PlantSerializer(serializers.ModelSerializer):
    nursery = NurserySerializer(read_only=True)
    class Meta:
        model = Plants
        fields = ['name', 'price','image','nursery']


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    product = PlantSerializer(read_only=True)
    nursery =NurserySerializer(read_only=True)
    # product = serializers.RelatedField(source='plants.id',read_only=True)
    class Meta:
        model = Order
        fields = ['user_name', 'product','date_ordered','order_id','is_purchased','cost','quantity','nursery']
    # def create(self, validated_data):
    #     mod_data = validated_data.pop('product')
    #     nursery =Plants.objects.create(**validated_data)
    #     Order.objects.create(product=nursery,**mod_data)