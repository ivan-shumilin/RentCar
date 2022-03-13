# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
from django.contrib import admin
from .models import CarsClass, BodyType, Cars, CarInstance, Manufacturers, Transmission

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
    list_display = ('model', 'manufacturers', 'carsclass', 'bodytype', 'display_transmission')
    inlines = [CarInstanceInline]


@admin.register(CarInstance)
class CarInstanceAdmin(admin.ModelAdmin):
    list_display = ('cars', 'due_back', 'status')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('cars', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )