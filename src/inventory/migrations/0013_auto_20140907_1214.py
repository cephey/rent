# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20140906_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'verbose_name': 'contract', 'verbose_name_plural': 'contracts'},
        ),
        migrations.AddField(
            model_name='contract',
            name='total',
            field=models.CharField(max_length=32, null=True, verbose_name='Total', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contract',
            name='zip',
            field=models.CharField(max_length=16, null=True, verbose_name='Zip-package number', blank=True),
        ),
    ]
