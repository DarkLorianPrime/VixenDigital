# Generated by Django 4.2.2 on 2023-07-20 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_notifications_user_cart_user_favourite_user_logo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admin_code',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
