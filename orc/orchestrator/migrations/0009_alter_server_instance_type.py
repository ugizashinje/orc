# Generated by Django 4.1 on 2022-08-26 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0008_instancetype_server_instance_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='instance_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orchestrator.instancetype'),
        ),
    ]
