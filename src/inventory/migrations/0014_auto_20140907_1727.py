# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20140907_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.PositiveIntegerField()),
                ('equipment', models.ForeignKey(to='inventory.Equipment')),
                ('period', models.ForeignKey(to='inventory.Period')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='equipment',
            name='periods',
            field=models.ManyToManyField(to='inventory.Period', verbose_name='Prices', through='inventory.Prices'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contract',
            name='period',
            field=models.ForeignKey(help_text='Rental period', to='inventory.Period'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='count',
            field=models.PositiveIntegerField(default=0, verbose_name='Count', blank=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='hash',
            field=models.CharField(verbose_name='Hash', max_length=64, editable=False),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='inventory.EquipmentType'),
        ),
    ]
