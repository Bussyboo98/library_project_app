# Generated by Django 3.2.3 on 2024-02-07 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0004_auto_20240207_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='reason_for_borrowing',
            field=models.TextField(blank=True, null=True),
        ),
    ]
