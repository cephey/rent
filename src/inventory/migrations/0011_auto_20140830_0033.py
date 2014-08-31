# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_remove_reserveequipment_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveEA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField()),
                ('ea', models.ForeignKey(to='inventory.EA')),
                ('reserve', models.ForeignKey(to='inventory.Reserve')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reserve',
            name='eas',
            field=models.ManyToManyField(to=b'inventory.EA', through='inventory.ReserveEA'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserve',
            name='status',
            field=models.CharField(default=b'NEW', max_length=4, choices=[(b'NEW', '\u041d\u043e\u0432\u044b\u0439'), (b'RES', '\u0413\u043e\u0442\u043e\u0432\u044b\u0439 \u043a \u043e\u043f\u043b\u0430\u0442\u0435'), (b'PAID', '\u041e\u043f\u043b\u0430\u0447\u0435\u043d\u043e')]),
        ),
    ]
