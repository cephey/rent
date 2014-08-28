# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20140827_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserveequipment',
            name='equipment',
            field=models.ForeignKey(to='inventory.Equipment'),
        ),
    ]
