# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_reserve'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='general',
            field=models.BooleanField(default=False, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0435'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='hash',
            field=models.CharField(verbose_name='\u0425\u0435\u0448', max_length=64, editable=False),
        ),
    ]
