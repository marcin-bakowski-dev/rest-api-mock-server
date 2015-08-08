# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_time', models.TimeField(auto_now_add=True)),
                ('user_agent', models.CharField(default=b'', max_length=254, blank=True)),
                ('path', models.CharField(max_length=254)),
                ('request_method', models.CharField(max_length=10)),
                ('request_headers', models.TextField(default=b'', blank=True)),
                ('request_data', models.TextField(default=b'', blank=True)),
                ('response_status_code', models.IntegerField()),
                ('response_headers', models.TextField(default=b'', blank=True)),
                ('response_content', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiEndpoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=254)),
                ('method', models.CharField(max_length=10)),
                ('status_code', models.IntegerField()),
                ('response', models.TextField(default=b'', blank=True)),
            ],
        ),
    ]
