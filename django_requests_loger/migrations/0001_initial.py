# Generated by Django 4.2.14 on 2024-11-12 14:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('hostname', models.CharField(blank=True, max_length=255, null=True)),
                ('method', models.CharField(max_length=10)),
                ('controller_action', models.CharField(blank=True, max_length=255, null=True)),
                ('middleware', models.CharField(blank=True, max_length=255, null=True)),
                ('path', models.CharField(max_length=500)),
                ('status_code', models.IntegerField()),
                ('duration', models.FloatField()),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('memory_usage', models.CharField(blank=True, max_length=50, null=True)),
                ('tags', models.TextField(blank=True, null=True)),
                ('headers', models.TextField()),
                ('body', models.TextField(blank=True, null=True)),
                ('response', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
