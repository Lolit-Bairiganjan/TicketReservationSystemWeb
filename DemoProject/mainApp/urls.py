from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('loginUser/', views.login_user, name='login_user'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_user, name='logout_user'),
    path('features/', views.features_page, name='features_page'),
    path('contacts/', views.contacts_page, name='contacts_page'),
    path('login/signup/', views.signup_page, name='signup_page'),
    path('registerUser/', views.register_user, name='register_user'),
    path('pnrStatus/', views.check_pnr_status, name='check_pnr_status'),
]
