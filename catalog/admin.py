# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
from django.contrib import admin
from .models import CarsClass, BodyType, Cars, CarInstance, Manufacturers, Transmission, Orders

admin.site.register(CarsClass)
admin.site.register(BodyType)
admin.site.register(Transmission)


class ManufacturersAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


admin.site.register(Manufacturers, ManufacturersAdmin)


class CarInstanceInline(admin.TabularInline):
    model = CarInstance


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('model', 'manufacturers', 'carsclass', 'bodytype', 'display_transmission', 'price')
    inlines = [CarInstanceInline]

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_instance', 'date_start', 'date_finish', 'place_start', 'place_finish', 'comments')



@admin.register(CarInstance)
class CarInstanceAdmin(admin.ModelAdmin):
    list_display = ('cars', 'id')
    # list_filter = ('date_start', 'date_finish')
    #
    # fieldsets = (
    #     (None, {
    #         'fields': ('cars', 'id')
    #     }),
    #     ('Availability', {
    #         'fields': ('borrower', 'date_start', 'date_finish')
    #     }),
    # )