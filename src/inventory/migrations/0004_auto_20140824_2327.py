# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20140824_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ea',
            name='hash',
            field=models.CharField(unique=True, max_length=64, verbose_name='\u0425\u0435\u0448'),
        ),
    ]
