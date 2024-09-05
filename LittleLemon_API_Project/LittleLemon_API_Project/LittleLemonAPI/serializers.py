from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id','title','slug']

class MenuItemsSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model  = MenuItem
        fields = ['id','title','price','featured','category']



class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs
    
    class Meta:
        model  = Cart
        fields = ['id','user','menuitem','quantity','unit_price','price']
        

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    delivery_crew = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model  = Order
        fields = ['user','delivery_crew','status','total','date']


        
class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    class Meta:
        model  = OrderItem
        fields = ['order','menuitem','quantity','price']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model    = User
        fields = ['id','username','email']