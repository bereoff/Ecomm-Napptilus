# Generated by Django 5.0 on 2023-12-10 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_productattributevalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(choices=[('pending', 'Pending'), ('purchased', 'Purchased')], default='pending', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='products_cart', through='checkout.CartProduct', to='checkout.product'),
        ),
    ]