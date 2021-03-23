from django.urls import path

from ticaret import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('signup', views.signup, name="signup"),
    path('userpage', views.userpage, name='userpage'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('log', views.log, name='log'),
]
