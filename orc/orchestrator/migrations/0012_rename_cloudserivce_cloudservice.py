# Generated by Django 4.1 on 2022-09-14 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0011_serverrequest_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CloudSerivce',
            new_name='CloudService',
        ),
    ]
