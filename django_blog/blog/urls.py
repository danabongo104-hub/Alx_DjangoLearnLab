from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='blog-home'),
    # authenitfication urls
    path('register/', views.registerPage, name='blog-register'),
    path('profile/', views.profile, name='blog-profile'),
    path('login/', views.login_view, name='blog-login'),
    path('logout/', views.logout_view, name='blog-logout'),
]