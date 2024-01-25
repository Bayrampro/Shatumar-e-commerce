# Generated by Django 5.0.1 on 2024-01-23 04:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Имя')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Имя')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Имя')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Имя')),
                ('content', models.TextField(verbose_name='Описания')),
                ('content_en', models.TextField(null=True, verbose_name='Описания')),
                ('content_ru', models.TextField(null=True, verbose_name='Описания')),
                ('img', models.ImageField(upload_to='photos/%Y/%m/')),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.category')),
                ('category_en', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.category')),
                ('category_ru', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.category')),
                ('likes', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
