# Generated by Django 4.2.14 on 2024-11-13 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='cache_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
