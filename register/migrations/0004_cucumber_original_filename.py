# Generated by Django 3.0.6 on 2020-06-30 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20200628_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='cucumber',
            name='original_filename',
            field=models.CharField(max_length=200, null=True),
        ),
    ]