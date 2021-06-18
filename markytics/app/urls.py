from django.urls import path
from app import views

urlpatterns = [
   
    path('',views.home,name='home'),
    path('login/',views.login, name='login'),
    path('reportform/',views.report,name='reportform'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout')
]
