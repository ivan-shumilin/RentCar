# Generated by Django 4.0.3 on 2022-03-16 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_carinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]