# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20140826_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserveequipment',
            name='equipment',
            field=models.ForeignKey(blank=True, to='inventory.Equipment', null=True),
        ),
    ]
