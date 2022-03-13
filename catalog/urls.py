from django.urls import path
from . import views
# from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.CarsListView.as_view(), name='cars'),
    path('cars/<pk>', views.CarsDetailView.as_view(), name='cars-detail'),
]
