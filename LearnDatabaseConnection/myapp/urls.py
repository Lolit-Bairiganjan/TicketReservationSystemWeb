from . import views
from django.urls import path

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
