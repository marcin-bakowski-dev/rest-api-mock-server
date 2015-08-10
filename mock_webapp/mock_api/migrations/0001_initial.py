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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('request_time', models.TimeField(auto_now_add=True)),
                ('user_agent', models.CharField(max_length=254, blank=True, default='')),
                ('path', models.CharField(max_length=254)),
                ('request_method', models.CharField(max_length=10)),
                ('request_headers', models.TextField(blank=True, default='')),
                ('request_query_string', models.TextField(blank=True, default='')),
                ('request_data', models.TextField(blank=True, default='')),
                ('response_status_code', models.IntegerField()),
                ('response_headers', models.TextField(blank=True, default='')),
                ('response_content', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='ApiCallback',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('method', models.CharField(max_length=10)),
                ('params', models.TextField(blank=True, default='')),
                ('headers', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='ApiEndpoint',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('path', models.CharField(max_length=254)),
                ('method', models.CharField(max_length=10)),
                ('callbacks', models.ManyToManyField(blank=True, to='mock_api.ApiCallback')),
            ],
        ),
        migrations.CreateModel(
            name='ApiResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('status_code', models.IntegerField()),
                ('content', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='ApiResponseRule',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('rule', models.CharField(max_length=50)),
                ('param_name', models.CharField(max_length=100, blank=True, default='')),
                ('param_value', models.CharField(max_length=100, blank=True, default='')),
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
            field=models.ManyToManyField(blank=True, to='mock_api.ApiResponseRule'),
        ),
        migrations.AddField(
            model_name='accesslog',
            name='api_endpoint',
            field=models.ForeignKey(to='mock_api.ApiEndpoint', null=True, blank=True),
        ),
    ]
