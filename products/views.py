from django.shortcuts import render
from rest_framework.response import Response
from products.models import Products,Reviews,Carts
from products.serializers import ReviewSerializer,ProductSerializer,CartSerializer,UserSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import authentication,permissions


# Create your views here.


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ProductView(ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Products.objects.all()

    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Products.objects.get(id=id)
        Reviews.objects.create(product=product,user=request.user,
                               comment=request.data.get("comment"),
                               rating=request.data.get("rating"))
        return Response(data="created")


    @action(methods=["POST"],detail=True)
    def addto_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Products.objects.get(id=id)
        Carts.objects.create(product=product,user=request.user)
        return Response(data="created")


    @action(methods=["GET"],detail=True)
    def cart_list(self,request,*args,**kwargs):
        cart=Carts.objects.all()
        cart_list=cart.products_set.all()
        serializer=CartSerializer(cart_list,many=True)
        return Response(data=serializer.data)


    @action(methods=["GET"],detail=True)
    def get_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Products.objects.get(id=id)
        reviews=product.reviews_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data)    

class ReviewView(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()
    def list(self, request, *args, **kwargs):
        all_reviews=Reviews.objects.all()
        if 'user' in request.query_params:
            all_reviews=all_reviews.filter(user=request.query_params.get("user"))
        serializer = ReviewSerializer(all_reviews, many=True)
        return Response(data=serializer.data)        