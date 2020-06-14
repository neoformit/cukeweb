# Generated by Django 3.0.6 on 2020-06-14 06:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20200614_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchrecord',
            name='failed',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='matchrecord',
            name='matches',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]