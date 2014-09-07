# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_auto_20140830_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deposit', models.CharField(default=b'DOC', max_length=4, verbose_name='Deposit', choices=[(b'MON', '\u0414\u0435\u043d\u044c\u0433\u0438'), (b'DOC', '\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b')])),
                ('zip', models.PositiveIntegerField(null=True, verbose_name='Zip-package number', blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='Period')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contract',
            name='period',
            field=models.ForeignKey(to='inventory.Period'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='reserve',
            field=models.ForeignKey(to='inventory.Reserve'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserve',
            name='status',
            field=models.CharField(default=b'NEW', max_length=4, choices=[(b'NEW', '\u041d\u043e\u0432\u044b\u0439'), (b'RES', '\u0413\u043e\u0442\u043e\u0432 \u043a \u043e\u043f\u043b\u0430\u0442\u0435'), (b'PAID', '\u041e\u043f\u043b\u0430\u0447\u0435\u043d\u043e')]),
        ),
    ]
