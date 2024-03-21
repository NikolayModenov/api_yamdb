# Generated by Django 3.2 on 2024-03-21 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20240320_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yamdbuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='адрес электронной почты'),
        ),
        migrations.AlterField(
            model_name='yamdbuser',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='Пользователь', max_length=9),
        ),
    ]
