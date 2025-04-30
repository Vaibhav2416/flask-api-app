from rest_framework import serializers
from .models import Product,Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['text','rating']

class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField(max_length=100)
    price=serializers.IntegerField()
    quantity=serializers.IntegerField()
    review_set=ReviewSerializer(many=True,read_only=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Product
#         fields=["id","name","price","quantity"]

