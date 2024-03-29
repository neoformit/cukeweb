# Generated by Django 3.0.6 on 2020-06-18 05:42

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import match.filename
import match.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(default=match.models.generate_matchset_id, max_length=100, unique=True)),
                ('targets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=75), null=True, size=None)),
                ('tank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Tank')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(default=match.models.generate_result_id, max_length=100, unique=True)),
                ('query_image', models.ImageField(upload_to=match.filename.image_upload_path)),
                ('score', models.FloatField(null=True)),
                ('is_target', models.BooleanField(default=False)),
                ('rejected_matches', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('backup_matches', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('backup_index', models.IntegerField(default=0)),
                ('exception', models.TextField(null=True)),
                ('traceback', models.TextField(null=True)),
                ('best_match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='register.Cucumber')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='match.MatchRecord')),
            ],
        ),
    ]
