# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20140826_0112'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e')),
                ('equipment', models.ForeignKey(to='inventory.Equipment')),
                ('reserve', models.ForeignKey(to='inventory.Reserve')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reserve',
            name='equipments',
            field=models.ManyToManyField(to=b'inventory.Equipment', through='inventory.ReserveEquipment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reserve',
            name='status',
            field=models.CharField(default=b'NEW', max_length=4, choices=[(b'NEW', b'Freshman'), (b'RES', b'Sophomore'), (b'PAID', b'Junior')]),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='eas',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='paid',
        ),
    ]
