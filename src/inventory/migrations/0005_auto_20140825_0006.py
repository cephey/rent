# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20140824_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ea',
            name='type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='inventory.EquipmentType'),
        ),
    ]
