from django.urls import path
from . import views
# from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.CarsListView.as_view(), name='cars'),
    path('cars/<pk>', views.CarsDetailView.as_view(), name='cars-detail'),
    path('manufacturers/', views.ManufacturersListView.as_view(), name='manufacturers'),
    path('manufacturers/<pk>', views.ManufacturersDetailView.as_view(), name='manufacturers-detail'),
    path('mybooks/', views.CarInstanceUserListView.as_view(), name='my-borrowed'),
]

