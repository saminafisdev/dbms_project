# Generated by Django 5.1.2 on 2024-10-14 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='/products/default.jpg', upload_to='products/'),
        ),
    ]
