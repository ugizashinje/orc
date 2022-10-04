# Generated by Django 4.1 on 2022-09-29 10:39

from django.db import migrations, models
import orchestrator.constants


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0013_remove_serverrequest_name_serverrequest_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverrequest',
            name='status',
            field=models.CharField(default=orchestrator.constants.SERVER_REQUEST.Status['PENDING'], max_length=16),
        ),
    ]