from rest_framework import serializers
from products.models import Products,Reviews,Carts
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True) 
    class Meta:
        model=Products
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    create_date=serializers.CharField(read_only=True)
    class Meta:
        model=Reviews
        fields="__all__"        


class CartSerializer(serializers.ModelSerializer):
    product=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model=Carts
        field=["product","user","status"]        

