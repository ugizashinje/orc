# Generated by Django 4.1 on 2022-08-26 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0003_serverrequest_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudSerivce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='server',
            name='cloud_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.CreateModel(
            name='CloudServiceProperties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
                ('cloud_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orchestrator.cloudserivce')),
            ],
        ),
    ]
