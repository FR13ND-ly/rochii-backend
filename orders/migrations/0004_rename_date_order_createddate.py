# Generated by Django 5.0.4 on 2024-05-09 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_message_order_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='createdDate',
        ),
    ]
