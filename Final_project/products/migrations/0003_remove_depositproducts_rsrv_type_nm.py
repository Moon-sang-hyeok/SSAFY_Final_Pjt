# Generated by Django 4.2.16 on 2024-11-21 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_depositproducts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositproducts',
            name='rsrv_type_nm',
        ),
    ]