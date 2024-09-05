from rest_framework import generics, status , viewsets, authentication
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemsSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group, User


# Create your views here.
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    search_fields    = ['category__title']
    ordering_fields  = ['price', 'inventory']
    
    def post(self, request):
        if self.request.user.is_superuser:
            return Response({"message":"new menu item created"}, 201)
        elif self.request.user.groups.filter(name='Manager').exists():
            return Response({"message":"new menu item created"}, 201)
        else:
            return Response({"message":"Unauthorized"}, 403)
                        

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

		
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN) 
        
    def put(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            instance = self.get_object()
            instance.delete()
            id = kwargs['pk']
            return Response({"message": f"Menu Item {id} Deleted"}, status=200)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)



class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        users = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response({"message": "User added to the manager group"}, status=200)

    def destroy(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        return Response({"message": "User removed from the manager group"}, status=200)


class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = User.objects.filter(groups__name='Delivery Crew')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        if not self.request.user.is_superuser and not self.request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        dc = Group.objects.get(name='Delivery Crew')
        dc.user_set.add(user)
        return Response({"message": "User added to the delivery crew group"}, status=200)

    def destroy(self, request):
        if not self.request.user.is_superuser and not self.request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        dc = Group.objects.get(name='Delivery Crew')
        dc.user_set.remove(user)
        return Response({"message": "User removed from the delivery crew group"}, status=200)



class CartView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user) #Sets Authenticated User As User Id For Cart Items
        self.perform_create(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        # Delete the entire collection
        self.get_queryset().delete()
        return Response({"message": "Entire Collection Deleted"}, status=status.HTTP_204_NO_CONTENT)


class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0:       #Customer - No Group
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        
    
    def create_order_items(self,request,*args,**kwargs):
        order_items_count = Cart.objects.all().filter(user=self.reqest.user).count()
        if order_items_count == 0:
            return Response({"message:":"No Items In Cart"})

        data = request.data.copy() 
        total            = self.get_total_price(self.request.user)
        data['total']    = total
        data['user']     = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if (order_serializer.is_valid()):
            order        = order_serializer.save()

            items       = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem      = OrderItem(
                    order      = order,
                    menuitem_id= item['menuitem_id'],
                    price      = item['price'],
                    quantity   = item['quantity'],
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

            result          = order_serializer.data.copy()
            result['total'] = total
            return Response(order_serializer.data)

    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total


class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset           = Order.objects.all()
    serializer_class   = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: #Customer - No Group
            return Response('Not Ok')
        else: # Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)
        