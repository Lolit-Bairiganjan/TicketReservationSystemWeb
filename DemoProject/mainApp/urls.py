from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.login_page, name='login_page'),
    path('login-user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('features/', views.features_page, name='features_page'),
    path('contacts/', views.contacts_page, name='contacts_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('register/', views.register_user, name='register_user'),
    
    # Booking flow - ALL require parameters
    path('book/search/', views.select_destinations, name='select_destinations'),
    path('book/schedules/<int:train_id>/<int:from_station_id>/<int:to_station_id>/', views.schedule_list, name='schedule_list'),
    path('book/select-schedule/<int:schedule_id>/<int:from_station_id>/<int:to_station_id>/', views.select_schedule, name='select_schedule'),
    path('book/ticket/<int:schedule_id>/<int:from_station_id>/<int:to_station_id>/', views.book_ticket, name='book_ticket'),
    
    # Ticket management
    path('ticket/<str:pnr>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<str:pnr>/add-passengers/', views.add_passengers, name='add_passengers'),
    path('ticket/<str:pnr>/cancel/', views.cancel_ticket, name='cancel_ticket'),
    path('check-pnr/', views.check_pnr_status, name='check_pnr_status'),
    
    # Utility
    path('clear-session/', views.clear_ticket_session, name='clear_ticket_session'),
]
