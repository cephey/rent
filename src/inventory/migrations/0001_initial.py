# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count_in', models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043d\u0430 \u0441\u043a\u043b\u0430\u0434\u0435', blank=True)),
                ('count_out', models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432 \u0430\u0440\u0435\u043d\u0434\u0435', blank=True)),
                ('hash', models.CharField(max_length=64, verbose_name='\u0425\u0435\u0448')),
            ],
            options={
                'ordering': [b'type'],
                'verbose_name': 'unit',
                'verbose_name_plural': 'units',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.CharField(max_length=16, verbose_name='\u041a\u043e\u0434 \u0442\u043e\u0432\u0430\u0440\u0430')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('hash', models.CharField(max_length=64, verbose_name='\u0425\u0435\u0448')),
            ],
            options={
                'ordering': [b'type'],
                'verbose_name': 'equipment',
                'verbose_name_plural': 'equipments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': [b'name'],
                'verbose_name': 'equipment type',
                'verbose_name_plural': 'equipment types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='inventory.EquipmentType'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
                ('equipment', models.ForeignKey(verbose_name='\u041e\u0431\u043e\u0440\u0443\u0434\u043e\u0432\u0430\u043d\u0438\u0435', to='inventory.Equipment')),
            ],
            options={
                'ordering': [b'type'],
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': [b'name'],
                'verbose_name': 'property type',
                'verbose_name_plural': 'type of properties',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='property',
            name='type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='inventory.PropertyType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ea',
            name='type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='inventory.PropertyType'),
            preserve_default=True,
        ),
    ]
