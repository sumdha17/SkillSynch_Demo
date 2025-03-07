# Generated by Django 5.1.6 on 2025-02-27 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_customuser_designation'),
        ('utils', '0008_alter_choice_choice_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='grade',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='roll',
            field=models.ForeignKey(limit_choices_to={'choice_type': 'assignee'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee_type', to='utils.choice'),
        ),
    ]
