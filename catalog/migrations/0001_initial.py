# Generated by Django 4.0.3 on 2022-03-12 17:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='Enter a car body style', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CarsClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a car type (e.g. Business Class)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name', 'country'],
            },
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=200)),
                ('bodytype', models.ManyToManyField(help_text='Select body type', to='catalog.bodytype')),
                ('carsclass', models.ManyToManyField(help_text='Choose a class for this car', to='catalog.carsclass')),
                ('manufacturers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.manufacturers')),
            ],
            options={
                'ordering': ['model', 'manufacturers'],
            },
        ),
        migrations.CreateModel(
            name='CarInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular car across whole catelog RentCar', primary_key=True, serialize=False)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='m', help_text='Car availability', max_length=1)),
                ('cars', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.cars')),
            ],
            options={
                'ordering': ['date_start'],
            },
        ),
    ]
