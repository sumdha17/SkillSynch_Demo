# Generated by Django 5.1.6 on 2025-02-20 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('choice_name', 'choice_type')},
        ),
    ]
