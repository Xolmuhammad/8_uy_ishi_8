from rest_framework.routers import SimpleRouter, DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register('brands', BrandViewSet, basename='brands')
router.register('cars', CarViewSet,basename='cars')


urlpatterns = router.urls