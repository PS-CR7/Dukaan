from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .services import UserService
from .models import *
from django.db import transaction


class UserViewSet(GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post"]
    serializers_dict = {
    }

    @transaction.atomic()
    @action(
        methods=["post"], detail=False, authentication_classes=[], permission_classes=[]
    )
    def login(self, request):
        data = request.data
        mobile = data.get('mobile')
        password = data.get('otp')
        user = UserService.get_user(mobile=mobile)
        if not user:
            return Response({
                'status':400, 'message':'User does not exists'
            })
        if user:
            return Response({"token": str(mobile)[-6:]+str(password)})
        return Response({
                'status':400, 'message':'User does not exists'
            })

    @transaction.atomic()
    @action(
        methods=["post"], detail=False, authentication_classes=[], permission_classes=[]
    )
    def signup(self, request):
        data = request.data
        response = UserService.create_signup(data)
        return Response(response)
    
    @transaction.atomic()
    @action(
        methods=["post"], detail=False,
    )
    def create_store(self, request):
        data = request.data
        store_data={}
        store_data['customer'] = request.user
        store_data['store_name']=data.get('store_name')
        store_data['address']=data.get('address')
        info= Store.objects.create(**store_data)
        
        return Response({'store_id':info.id, 'store_link':info.store_link})

    @transaction.atomic()
    @action(methods=["post"], detail=False,)
    def create_product(self, request):
        data = request.data
        prod_data={}
        prod_data['store'] = Store.objects.get(store_link= data.get('store_link'))
        prod_data['product_name']=data.get('product_name')
        prod_data['category']=data.get('category')
        prod_data['mrp']=data.get('mrp')
        prod_data['description']=data.get('description')
        prod_data['sale_price']=data.get('sale_price')
        prod_data['image']=data.get('image')
        info= Product.objects.create(**prod_data)
        
        return Response({'product_id':info.id, 'product_name':info.product_name,
                        'product_image':info.image})


    @transaction.atomic()
    @action(methods=["post"], detail=False,authentication_classes=[], permission_classes=[])
    def create_customer(self, request):
        data = request.data
        cust_data={}
        cust_data['mobile']=data.get('mobile')
        cust_data['first_name']=data.get('first_name')
        cust_data['last_name']=data.get('last_name')
        cust_data['address']=data.get('address')
        user = Customer.objects.filter(mobile= cust_data['mobile'])
        if not user:
            info= Customer.objects.create(**cust_data)
        else:
            return Response({
                'status':400, 'message':'User already exists'
            })
        
        return Response({'customer_id':info.id})

    @transaction.atomic()
    @action(methods=["get"], detail=False,authentication_classes=[], permission_classes=[])
    def get_store(self, request):
        data = request.GET
        store_link=data.get('store_link')
        info= Store.objects.get(store_link=store_link)
        return Response({'store_id':info.id, 'store_name':info.store_name,
                        'address':info.address})

    @transaction.atomic()
    @action(methods=["get"], detail=False,authentication_classes=[], permission_classes=[])
    def get_product(self, request):
        data = request.GET
        store_link=data.get('store_link')
        
        info=[]
        store_info= Store.objects.get(store_link=store_link)
        store_data= Product.objects.filter(store=store_info)
        for data in store_data:
            info.append({'category':data.category,'product_name':data.product_name})

        group_data = sorted(info,key=lambda kv:kv['category'])
        # print(group_data)
        
        
        return Response({'all_data':group_data})

    @transaction.atomic()
    @action(methods=["post"], detail=False,authentication_classes=[], permission_classes=[])
    def create_cart(self, request):
        data = request.data
        info={}
        info['session']=data.get('session_id')
        # for item in data.get('items'):
        #     print(item)
        #     items_list.append({'product_id':item.product_id,'quantity':item.quantity,
        #             'category' : info.category})
        info['items']=data.get('items')
        cart_info = Cart.objects.create(**info)
        
        return Response({'all_data':cart_info.id})

    @transaction.atomic()
    @action(methods=["post"], detail=False,)
    def create_order(self, request):
        data = request.data
        order_data={}
        order_list=[]
        order_data['buyer']= Customer.objects.get(id=data.get('customer_id'))
        
        if not data.get('cart_id'):
            order_info= data.get('order_info')
            order_data['order_item'] = order_info
            
        else:
            cart_obj= Cart.objects.get(id=data.get('cart_id'))
            order_data['order_item'] = cart_obj.items

        order_obj= Order.objects.create(**order_data)
        
        return Response({'order_id':order_obj.id})

    



    
    

    
    
