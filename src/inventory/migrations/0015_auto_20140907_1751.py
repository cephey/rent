# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20140907_1727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prices',
            old_name='price',
            new_name='value',
        ),
    ]
