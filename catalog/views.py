from django.shortcuts import render
from .models import Transmission, CarsClass, BodyType, Cars, CarInstance, Manufacturers
from django.views import generic
from django.views.generic.detail import DetailView

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
    num_cars = Cars.objects.all().count()
    num_instances = CarInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = CarInstance.objects.filter(status__exact='a').count()
    num_manufacturers = Manufacturers.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_cars': num_cars, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_manufacturers': num_manufacturers},
    )


# https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/
class CarsListView(generic.ListView):
    model = Cars
    paginate_by = 10
    # template_name = 'catalog/cars.html'


class CarsDetailView(generic.DetailView):
    model = Cars
    paginate_by = 10

