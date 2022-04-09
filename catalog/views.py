from django.shortcuts import render
from .models import Transmission, CarsClass, BodyType, Cars, CarInstance, Manufacturers
from django.views import generic
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewCarForm, FindCarForm
from django.contrib.auth.decorators import permission_required
from django.db.models import Q


@permission_required('catalog.can_mark_returned')
def renew_car_manager(request, pk):
    """
    Функция просмотра для обновления определенного CarInstance менеджером
    """
    car_inst = get_object_or_404(CarInstance, pk=pk)

    if request.method == 'POST':
        # Создём экземпляр формы и заполняем его данными из запроса (binding):
        form = RenewCarForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            car_inst.date_start = form.cleaned_data['renewal_date']
            car_inst.save()
            return HttpResponseRedirect(reverse('all-users-cars'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewCarForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/car_renew_manager.html', {'form': form, 'carinst': car_inst})


def search_free_cars(form_date_start, form_date_finish):
    free_carInstance = CarInstance.objects.filter(
           Q(status = 'a') |
           Q (date_finish__lt=form_date_start) |
           Q (date_start__gt=form_date_finish))
    free_car = []
    for car in free_carInstance:
        free_car.append(f'{str(car.cars.manufacturers)} {str(car.cars.model)}')
    return list(set(free_car))

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # форма поиска автомобиля
    errors = None
    if request.method == 'POST':
        user_form = FindCarForm(request.POST)
        if user_form.is_valid():
            free_cars = search_free_cars(user_form.cleaned_data["date_start"], user_form.cleaned_data["date_finish"])
        return render(request, 'index.html', {'user_form': user_form,
                                              'errors': errors,
                                              'free_cars': free_cars})
    user_form = FindCarForm()
    # Отрисовка HTML-шаблона index.html с данными внутри
    return render(request, 'index.html', {'user_form': user_form, 'errors': errors})

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

def statistic(request):
    # Генерация "количеств" некоторых главных объектов
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
    num_cars = Cars.objects.all().count()
    num_instances = CarInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = CarInstance.objects.filter(status__exact='a').count()
    num_manufacturers = Manufacturers.objects.count()  # Метод 'all()' применён по умолчанию.
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'num_cars': num_cars,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_manufacturers': num_manufacturers,
               'num_visits': num_visits }

    # Отрисовка HTML-шаблона index.html с данными внутри
    return render(request, 'catalog/statistic.html', context)


# https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/
class CarsListView(generic.ListView):
    model = Cars
    paginate_by = 10
    # template_name = 'catalog/cars.html'


class CarsDetailView(generic.DetailView):
    model = Cars
    paginate_by = 10


class CarInstanceUserListView(LoginRequiredMixin, generic.ListView):
    """
    Общий список автомобилей предоставленных в аренду текущему пользователю.
    """
    model = CarInstance
    template_name = 'catalog/carinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return CarInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('date_start')


class CarInstanceManagerListView(PermissionRequiredMixin, generic.ListView):
    """
    Общий список автомобилей предоставленных в аренду всем пользователям.
    """
    model = CarInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/carinstance_list_borrowed_manager.html'
    paginate_by = 10

    def get_queryset(self):
        return CarInstance.objects.filter(status__exact='o').order_by('date_start')


class ManufacturersListView(generic.ListView):
    model = Manufacturers
    paginate_by = 10


class ManufacturersDetailView(generic.DetailView):
    model = Manufacturers
    paginate_by = 10


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Cars


# https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-editing/
class CarCreate(PermissionRequiredMixin, CreateView):
    model = Cars
    fields = ['model', 'manufacturers', 'transmission', 'bodytype', ]
    initial = {'bodytype': 'sport'}
    permission_required = 'catalog.can_mark_returned'


class CarUpdate(PermissionRequiredMixin, UpdateView):
    model = Cars
    fields = ['model', 'manufacturers', 'transmission', 'bodytype', ]
    permission_required = 'catalog.can_mark_returned'


class CarDelete(PermissionRequiredMixin, DeleteView):
    model = Cars
    success_url = reverse_lazy('cars')  # редирект на страницу cars/
    permission_required = 'catalog.can_mark_returned'
