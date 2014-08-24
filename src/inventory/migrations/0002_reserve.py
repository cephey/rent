# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eas', models.ManyToManyField(to='inventory.EA')),
                ('user', models.ForeignKey(verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reserve',
                'verbose_name_plural': 'reserve',
            },
            bases=(models.Model,),
        ),
    ]
