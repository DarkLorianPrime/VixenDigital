# Generated by Django 4.2.2 on 2023-07-11 18:57

from django.db import migrations, models
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0008_alter_organization_logo_alter_organization_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.ImageField(storage=django_minio_backend.models.MinioBackend(bucket_name='private-bucket'), upload_to=''),
        ),
    ]