from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('ticket/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket_view, name='edit_ticket'),
    path('create-ticket/', views.create_ticket_view, name='create_ticket'),
    path('forbidden/', views.forbidden_view, name='forbidden'),
]

