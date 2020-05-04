# Generated by Django 3.0.5 on 2020-04-30 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product'),
        ('reviews', '0004_remove_review_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product'),
        ),
    ]
