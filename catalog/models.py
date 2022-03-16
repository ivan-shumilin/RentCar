from django.db import models
from django.urls import reverse
import uuid  # Required for unique car instances
from django.contrib.auth.models import User
from datetime import date


class Transmission(models.Model):
    """Model representing transmission type."""
    transmission = models.CharField(max_length=200, help_text='Enter the type of transmission')

    def __str__(self):
        return self.transmission

class CarsClass(models.Model):
    """A model that represents the car of the class."""
    name = models.CharField(max_length=200, help_text='Enter a car type (e.g. Business Class)')

    def __str__(self):
        return self.name


class BodyType(models.Model):
    """Model representing a body style."""
    type = models.CharField(max_length=200, help_text='Enter a car body style')

    def __str__(self):
        return self.type


class Cars(models.Model):
    """Model representing a cars (but not a specific copy of a car)."""
    model = models.CharField(max_length=200)
    manufacturers = models.ForeignKey('Manufacturers', on_delete=models.SET_NULL, null=True)
    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey.on_delete
    # on_delete  определяет что делать, если удалился связанный объект
    # SET_NULL посты останутся в БД даже при удалении manufacturers,
    # но значение в поле manufacturers у постов изменится на None
    carsclass = models.ForeignKey('CarsClass', on_delete=models.SET_NULL, null=True, help_text='Choose a class for this car')
    bodytype = models.ForeignKey('BodyType', on_delete=models.SET_NULL, null=True, help_text='Select body type')
    transmission = models.ManyToManyField(Transmission, help_text='the type of transmission')

    class Meta:
        ordering = ['model', 'manufacturers']
    # https://docs.djangoproject.com/en/4.0/ref/models/options/#model-meta-options

    def get_absolute_url(self):
        return reverse('cars-detail', args=[str(self.id)])

    def display_transmission(self):
        """Creates a string for the type transmission. This is required to display type in Admin."""
        return ', '.join([transmission.transmission for transmission in self.transmission.all()[:3]])

    display_transmission.short_description = 'Type transmission'

    def __str__(self):
        return self.model


class CarInstance(models.Model):
    """Model representing a specific copy of a car (i.e. that can be rent in RentCar)."""
    # UUIDField https://docs.djangoproject.com/en/4.0/ref/models/fields/
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular car across whole catelog RentCar')
    # Предотвратите удаление объекта, на который ссылаются, путем повышения RestrictedError
    # (подкласс django.db.IntegrityError). В отличие от PROTECT, удаление объекта, на который
    # указывает ссылка, разрешено, если он также ссылается на другой объект, который удаляется в той же операции,
    # но через CASCADE отношение.
    cars = models.ForeignKey('Cars', on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Car availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.cars.manufacturers} {self.cars.model}, ID:{self.id}'


class Manufacturers(models.Model):
    """Model representing a manufacturers."""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        ordering = ['name', 'country']

    def get_absolute_url(self):
        return reverse('manufacturers-detail', args=[str(self.id)])

    def __str__(self):
        return self.name