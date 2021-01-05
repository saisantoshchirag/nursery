from django.shortcuts import render,redirect
from .models import Plants,Order,Nursery
from django.contrib import messages
import uuid
from django.contrib.auth.decorators import login_required
from rest_framework import permissions,generics
from .serializers import PlantSerializer,OrderSerializer
from accounts.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
@login_required(login_url='/accounts/login/')

def home(request):
    obj = Plants.objects.all()
    prof = Profile.objects.get(user=request.user)
    user_type = prof.type
    is_nur = True if str(user_type) == 'Nursery' else False
    try:
        nursery = Nursery.objects.get(profile=prof)
        has_nur = True
    except:
        has_nur = False
    return render(request,'nursery/nursery.html',{'plants':obj,'is_nur':is_nur,'has_nur':has_nur})

def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        img = request.FILES['image']
        nur_id = request.POST['nursery']
        try:
            Plants.objects.get(name=name)
            messages.success(request,'Plant already exitsts')
            return redirect('nursery:add')
        except:
            Plants.objects.create(name=name,price=price,image=img,nursery_id=nur_id)
            return redirect('nursery:home')
    else:
        nurseries = Nursery.objects.all()
        return render(request,'nursery/add_product.html',{'nurseries':nurseries})

@login_required(login_url='/accounts/login')
def add_to_cart(request,product):
    id = uuid.uuid4()
    plant = Plants.objects.get(name=product)
    Order.objects.create(product=plant,user=request.user,cost=plant.price,order_id=id,quantity=1,nursery=plant.nursery)
    return redirect('nursery:home')

def add_nursery(request):
    if request.method == 'POST':
        name = request.POST['name']
        state = request.POST['state']
        city = request.POST['city']
        prof = Profile.objects.get(user=request.user)
        Nursery.objects.create(name=name,state=state,city=city,profile=prof)
        return redirect('nursery:home')
    else:
        user = Profile.objects.get(user=request.user)
        # try:
        #     nursery = Nursery.objects.get(profile=user)
        # except:
        #
        if user.type == 'User':
            messages.success(request,'Operation Not allowed')
            return redirect('nursery:home')
    return render(request,'nursery/add_nur.html')

@login_required(login_url='/accounts/login')
def cart(request):
    prods = Order.objects.filter(user=request.user,is_purchased=False)
    return render(request,'nursery/cart.html',{'products':prods})

def change_quan(request,product,quan,mode):
    sign = 1 if mode == 'plus' else -1
    prod = Plants.objects.get(name=product)
    updated_quan = sign+int(quan)
    Order.objects.filter(product__name=product,user=request.user).update(quantity = updated_quan,cost = prod.price*(updated_quan))
    return redirect('nursery:shopping_cart')

def checkout(request):
    Order.objects.filter(user=request.user).update(is_purchased=True)
    return redirect('nursery:shopping_cart')

def view_orders(request):
    prof = Profile.objects.get(user=request.user)
    nursery = Nursery.objects.get(profile=prof)
    obj = Order.objects.filter(nursery=nursery,is_purchased=True)

    return render(request,'nursery/view_order.html',{'objs':obj})


class PlantViewSet(generics.ListAPIView):
    queryset = Plants.objects.all()
    serializer_class = PlantSerializer


class PlantDetailSet(generics.ListAPIView):
    serializer_class = PlantSerializer
    def get_queryset(self):
        plant = self.kwargs['plant']
        return Plants.objects.filter(name=plant)


class OrderViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_queryset(self):
        nursery = Nursery.objects.get(name=self.kwargs['nursery'])
        return Order.objects.filter(nursery=nursery)

class PostOrder(APIView):
    serializer = OrderSerializer
    def post(self, request, format=None):
        data = request.data
        id = uuid.uuid4()

        data['order_id'] = id
        plant = Plants.objects.get(id=request.data['product'])

        data['cost'] = plant.price * request.data['quantity']
        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            Order.objects.create(product=plant, user=request.user, cost=data['cost'], order_id=id, quantity=request.data['quantity'], nursery=plant.nursery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)