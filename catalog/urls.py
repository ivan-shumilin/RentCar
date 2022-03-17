from django.urls import path
from . import views
# from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.CarsListView.as_view(), name='cars'),
    path('cars/<pk>', views.CarsDetailView.as_view(), name='cars-detail'),
    path('manufacturers/', views.ManufacturersListView.as_view(), name='manufacturers'),
    path('manufacturers/<pk>', views.ManufacturersDetailView.as_view(), name='manufacturers-detail'),
    path('mycars/', views.CarInstanceUserListView.as_view(), name='my-borrowed'),
    path('userscars', views.CarInstanceManagerListView.as_view(), name='all-users-cars'),
    path('cars/<pk>/renew/', views.renew_car_manager, name='renew-car-manager'),
    path('cars/create/', views.CarCreate.as_view(), name='car-create'),

]

