# Generated by Django 4.1 on 2022-08-26 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0006_rename_cloudserviceproperties_cloudserviceproperty'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cloudserviceproperty',
            options={'verbose_name_plural': 'CloudServiceProperties'},
        ),
    ]
