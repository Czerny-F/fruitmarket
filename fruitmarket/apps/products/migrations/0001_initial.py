# Generated by Django 2.0.4 on 2018-04-15 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='datetime updated')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='datetime created')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='name')),
                ('unit_price', models.PositiveIntegerField(verbose_name='unit price')),
            ],
            options={
                'verbose_name': 'fruit',
                'verbose_name_plural': 'fruits',
                'ordering': ['-updated_at', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='fruit',
            index=models.Index(fields=['updated_at', 'created_at'], name='products_fruit_timestamp_idx'),
        ),
    ]
