# Generated by Django 4.1 on 2022-08-25 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloud_id', models.CharField(blank=None, max_length=64, null=True)),
                ('status', models.CharField(max_length=16)),
            ],
        ),
    ]
