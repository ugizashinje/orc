# Generated by Django 4.1 on 2022-08-26 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0004_cloudserivce_alter_server_cloud_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='name',
            field=models.CharField(default='', max_length=128),
        ),
    ]
