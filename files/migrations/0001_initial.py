# Generated by Django 5.0.4 on 2024-04-26 18:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contentType', models.CharField(max_length=100)),
                ('data', models.BinaryField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]