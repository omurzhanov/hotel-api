# Generated by Django 3.1 on 2021-04-22 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210422_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(default='room/romeo.jpeg', upload_to='images'),
        ),
    ]
