from django.urls import path, include
from . import views

app_name = 'nursery'
urlpatterns = [
    path('',views.home,name='home'),
    path('nursery/add/',views.add,name='add'),
    path('nursery/cart/<str:product>',views.add_to_cart,name='cart'),
    path('nursery/add/nursery',views.add_nursery,name='add_nur'),
    path('cart',views.cart,name='shopping_cart'),
    path('checkout',views.checkout,name='checkout'),
    path('orders',views.view_orders,name='orders'),
    path('cart/<product>/<quan>/<mode>',views.change_quan,name='change'),
    path('plants/view',views.PlantViewSet.as_view()),
    path('plants/view/<plant>',views.PlantDetailSet.as_view()),
    path('orders/view/<nursery>',views.OrderViewSet.as_view()),
    path('orders/post',views.PostOrder.as_view()),


]