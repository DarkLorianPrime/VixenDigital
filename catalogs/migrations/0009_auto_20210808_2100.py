# Generated by Django 3.2.5 on 2021-08-08 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0008_features_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='features',
            name='required',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='main_categories',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogs.main_categories'),
        ),
    ]
