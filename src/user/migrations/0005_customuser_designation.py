# Generated by Django 5.1.6 on 2025-02-26 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_customuser_gender_alter_customuser_status_and_more'),
        ('utils', '0008_alter_choice_choice_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='designation',
            field=models.ForeignKey(blank=True, limit_choices_to={'choice_type': 'designation'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee_designation', to='utils.choice'),
        ),
    ]
