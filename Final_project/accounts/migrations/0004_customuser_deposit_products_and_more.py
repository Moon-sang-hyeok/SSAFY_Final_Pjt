# Generated by Django 4.2.16 on 2024-11-25 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_depositproducts_unique_together_and_more'),
        ('accounts', '0003_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='deposit_products',
            field=models.ManyToManyField(blank=True, related_name='subscribed_users', to='products.depositproducts'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='saving_products',
            field=models.ManyToManyField(blank=True, related_name='subscribed_users', to='products.savingproducts'),
        ),
    ]
