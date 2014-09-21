# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20140907_1751'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='period',
            options={'verbose_name': 'period', 'verbose_name_plural': 'periods'},
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='image',
            field=models.ImageField(default=b'', upload_to=b'equipment_type/'),
            preserve_default=True,
        ),
    ]
