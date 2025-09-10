from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api_v1'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet, basename='ticket')

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # API info
    path('info/', views.api_info, name='api_info'),
    
    # Include router URLs
    path('', include(router.urls)),
]
