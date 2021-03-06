# Generated by Django 4.0.3 on 2022-04-09 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_carinstance_date_finish'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_finish', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cars',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='carinstance',
            name='orders',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.orders'),
        ),
    ]
