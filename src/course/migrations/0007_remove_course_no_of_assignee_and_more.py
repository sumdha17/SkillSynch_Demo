# Generated by Django 5.1.6 on 2025-02-26 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_alter_assignee_designation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='no_of_assignee',
        ),
        migrations.AddField(
            model_name='questionoptions',
            name='is_correct',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
