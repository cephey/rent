# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20141003_0146'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('first_name', 'last_name', 'patronymic')]),
        ),
    ]
