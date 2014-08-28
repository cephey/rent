# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20140825_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='\u041e\u043f\u043b\u0430\u0442\u0438\u043b'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ea',
            name='hash',
            field=models.CharField(verbose_name='\u0425\u0435\u0448', unique=True, max_length=64, editable=False),
        ),
    ]
