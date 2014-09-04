# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'verbose_name': 'cards', 'verbose_name_plural': 'card'},
        ),
        migrations.AlterModelOptions(
            name='sms',
            options={'ordering': ['-create_at'], 'verbose_name': 'sms', 'verbose_name_plural': 'sms'},
        ),
        migrations.AddField(
            model_name='user',
            name='confirm',
            field=models.BooleanField(default=False, verbose_name='Phone confirm'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='article',
            field=models.CharField(help_text='\u0421\u043a\u0430\u043d\u0438\u0440\u0443\u0439\u0442\u0435 \u0448\u0442\u0440\u0438\u0445 \u043a\u043e\u0434 \u043a\u0430\u0440\u0442\u044b \u0434\u043b\u044f \u043f\u0440\u0438\u0432\u044f\u0437\u043a\u0438 \u0435\u0435 \u043a \u043a\u043b\u0438\u0435\u043d\u0442\u0443', max_length=16, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u043a\u0430\u0440\u0442\u044b'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
