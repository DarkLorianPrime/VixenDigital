# Generated by Django 4.2.2 on 2023-07-29 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0011_category_logo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Organization',
        ),
    ]