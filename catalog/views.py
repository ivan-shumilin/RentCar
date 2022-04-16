from django.shortcuts import render
from .models import Transmission, CarsClass, BodyType, Cars, CarInstance, Manufacturers, Orders
from django.views import generic
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewCarForm, FindCarsForm
from django.contrib.auth.decorators import permission_required
from django.db.models import Q


# @permission_required('catalog.can_mark_returned')
# def renew_car_manager(request, pk):
#     """
#     Функция просмотра для обновления определенного CarInstance менеджером
#     """
#     car_inst = get_object_or_404(CarInstance, pk=pk)
#
#     if request.method == 'POST':
#         # Создём экземпляр формы и заполняем его данными из запроса (binding):
#         form = RenewCarForm(request.POST)
#         # Check if the form is valid:
#         if form.is_valid():
#             car_inst.date_start = form.cleaned_data['renewal_date']
#             car_inst.save()
#             return HttpResponseRedirect(reverse('all-users-cars'))
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewCarForm(initial={'renewal_date': proposed_renewal_date, })
#
#     return render(request, 'catalog/car_renew_manager.html', {'form': form, 'carinst': car_inst})


def search_free_cars(form_date_start: datetime, form_date_finish: datetime):
    ''' Возвращает список моделей автомобилей которые свободны в эти даты'''
    free_car_instance: list = []
    cars = Cars.objects.all() # все авто
    for car in cars: # берем каждое авто
        for carinstance in car.carinstance_set.all(): # получаем все экземпляры этого авто и проходим по каждому
            orders = Orders.objects.filter(car_instance=carinstance) # полчаем сет заказов для конкретного экземпляра авто
            if len(orders) == 0:  # если нет заказов, добавляем экземпляр и переходим к следующему
                free_car_instance.append(carinstance)
                continue
            # проверяем свобен ли экземпляр авто в принятые даты
            for order in orders:
                order_date_start = order.date_start
                order_date_finish = order.date_finish
                latest_start = max(order_date_start, form_date_start)
                earliest_finish = min(order_date_finish, form_date_finish)
                if latest_start > earliest_finish:
                    free_car_instance.append(carinstance)
                    break
    # модели авто у которых есть свободные экземпляры на указанные даты
    free_car = set([car_instance.cars for car_instance in free_car_instance ])
    return free_car

def is_valid_custom(form_date_start, form_date_finish):
    errors = []
    if form_date_start > form_date_finish:
        errors.append('Дата начала аренды должна быть раньше даты конца аренды.')
    if form_date_start < datetime.date.today():
        errors.append('Извините, пока мы не можем отправить машину в прошлое.')
    return errors



def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # форма поиска автомобиля
    errors = []
    free_cars = []
    if request.method == 'POST':
        user_form = FindCarsForm(request.POST)
        if user_form.is_valid():
            errors = is_valid_custom(user_form.cleaned_data["date_start"], user_form.cleaned_data["date_finish"])
            if len(errors) == 0:
                free_cars = search_free_cars(user_form.cleaned_data["date_start"], user_form.cleaned_data["date_finish"])
            return render(request, 'index.html', {'user_form': user_form,
                                              'errors': errors,
                                              'free_cars': free_cars})
    user_form = FindCarsForm()
    # Отрисовка HTML-шаблона index.html с данными внутри
    return render(request, 'index.html', {'user_form': user_form, 'errors': errors})

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

# def statistic(request):
#     # Генерация "количеств" некоторых главных объектов
#     # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
#     num_cars = Cars.objects.all().count()
#     num_instances = CarInstance.objects.all().count()
#     num_manufacturers = Manufacturers.objects.count()  # Метод 'all()' применён по умолчанию.
#     # Number of visits to this view, as counted in the session variable.
#     num_visits = request.session.get('num_visits', 0)
#     request.session['num_visits'] = num_visits + 1
#     context = {'num_cars': num_cars,
#                'num_instances': num_instances,
#                'num_manufacturers': num_manufacturers,
#                'num_visits': num_visits }
#
#     # Отрисовка HTML-шаблона index.html с данными внутри
#     return render(request, 'catalog/statistic.html', context)


# https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/
class CarsListView(generic.ListView):
    model = Cars
    paginate_by = 10
    # template_name = 'catalog/cars.html'


class CarsDetailView(generic.DetailView):
    model = Cars
    paginate_by = 10

#
# class CarInstanceUserListView(LoginRequiredMixin, generic.ListView):
#     """
#     Общий список автомобилей предоставленных в аренду текущему пользователю.
#     """
#     model = CarInstance
#     template_name = 'catalog/carinstance_list_borrowed_user.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         return CarInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('date_start')
#
#
# class CarInstanceManagerListView(PermissionRequiredMixin, generic.ListView):
#     """
#     Общий список автомобилей предоставленных в аренду всем пользователям.
#     """
#     model = CarInstance
#     permission_required = 'catalog.can_mark_returned'
#     template_name = 'catalog/carinstance_list_borrowed_manager.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         return CarInstance.objects.filter(status__exact='o').order_by('date_start')


class ManufacturersListView(generic.ListView):
    model = Manufacturers
    paginate_by = 10


class ManufacturersDetailView(generic.DetailView):
    model = Manufacturers
    paginate_by = 10


# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from catalog.models import Cars


# https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-editing/
# class CarCreate(PermissionRequiredMixin, CreateView):
#     model = Cars
#     fields = ['model', 'manufacturers', 'transmission', 'bodytype', ]
#     initial = {'bodytype': 'sport'}
#     permission_required = 'catalog.can_mark_returned'
#
#
# class CarUpdate(PermissionRequiredMixin, UpdateView):
#     model = Cars
#     fields = ['model', 'manufacturers', 'transmission', 'bodytype', ]
#     permission_required = 'catalog.can_mark_returned'
#
#
# class CarDelete(PermissionRequiredMixin, DeleteView):
#     model = Cars
#     success_url = reverse_lazy('cars')  # редирект на страницу cars/
#     permission_required = 'catalog.can_mark_returned'
