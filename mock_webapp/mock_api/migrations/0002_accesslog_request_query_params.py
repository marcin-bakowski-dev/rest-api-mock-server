# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mock_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesslog',
            name='request_query_params',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
