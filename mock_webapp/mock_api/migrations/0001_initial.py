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
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('user_agent', models.CharField(default=b'', max_length=254, blank=True)),
                ('path', models.CharField(max_length=254)),
                ('request_method', models.CharField(max_length=10)),
                ('request_headers', models.TextField(default=b'', blank=True)),
                ('request_query_string', models.TextField(default=b'', blank=True)),
                ('request_data', models.TextField(default=b'', blank=True)),
                ('response_status_code', models.IntegerField()),
                ('response_headers', models.TextField(default=b'', blank=True)),
                ('response_content', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiCallback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('method', models.CharField(max_length=10)),
                ('params', models.TextField(default=b'', blank=True)),
                ('headers', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiEndpoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=254)),
                ('method', models.CharField(max_length=10)),
                ('callbacks', models.ManyToManyField(to='mock_api.ApiCallback', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('status_code', models.IntegerField()),
                ('content', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiResponseRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('rule', models.CharField(max_length=50)),
                ('param_name', models.CharField(default=b'', max_length=100, blank=True)),
                ('param_value', models.CharField(default=b'', max_length=100, blank=True)),
                ('response', models.ForeignKey(to='mock_api.ApiResponse')),
            ],
        ),
        migrations.AddField(
            model_name='apiendpoint',
            name='response',
            field=models.ForeignKey(to='mock_api.ApiResponse'),
        ),
        migrations.AddField(
            model_name='apiendpoint',
            name='response_rules',
            field=models.ManyToManyField(to='mock_api.ApiResponseRule', blank=True),
        ),
        migrations.AddField(
            model_name='accesslog',
            name='api_endpoint',
            field=models.ForeignKey(blank=True, to='mock_api.ApiEndpoint', null=True),
        ),
    ]
