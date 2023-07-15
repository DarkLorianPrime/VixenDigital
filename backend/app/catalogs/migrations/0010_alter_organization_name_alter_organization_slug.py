# Generated by Django 4.2.2 on 2023-07-11 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0009_alter_organization_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
