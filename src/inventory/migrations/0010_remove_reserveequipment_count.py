# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20140827_0153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserveequipment',
            name='count',
        ),
    ]
