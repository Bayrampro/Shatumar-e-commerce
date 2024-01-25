# Generated by Django 5.0.1 on 2024-01-23 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='brutto_weight',
            field=models.IntegerField(default=0, verbose_name='Вес брутто'),
        ),
        migrations.AddField(
            model_name='products',
            name='cost',
            field=models.IntegerField(default=0, verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='products',
            name='cost_for_box',
            field=models.IntegerField(default=0, verbose_name='Цена за каробку'),
        ),
        migrations.AddField(
            model_name='products',
            name='netto_weight',
            field=models.IntegerField(default=0, verbose_name='Вес нетто'),
        ),
        migrations.AddField(
            model_name='products',
            name='per_box',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='per_package',
            field=models.CharField(default=1, max_length=255, verbose_name='Ед. в упаковке'),
            preserve_default=False,
        ),
    ]
