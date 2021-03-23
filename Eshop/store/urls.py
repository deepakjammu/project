
from django.contrib import admin
from django.urls import path
from .views import  Index,Signup,Login, logout,Cart,CheckOut,OrderView


urlpatterns = [
   path('',Index.as_view(), name='index'),
   path('signup',Signup.as_view()),
   path('login',Login.as_view(), name='login'),
   path('logout',logout , name='logout' ),
   path('cart',Cart.as_view(), name='cart'),
   path('checkout', CheckOut.as_view(), name='checkout'),
   path('order', OrderView.as_view(), name='order'),
]
