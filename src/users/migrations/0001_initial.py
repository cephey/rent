# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('first_name', models.CharField(max_length=64, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=64, verbose_name='last name', blank=True)),
                ('patronymic', models.CharField(max_length=64, verbose_name='patronymic', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('passport', models.CharField(max_length=32, verbose_name='Number of passport', blank=True)),
                ('travel_passport', models.CharField(max_length=32, verbose_name='Travel passport number', blank=True)),
                ('drive_license', models.CharField(max_length=32, verbose_name="Driver's license number", blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('phone', models.CharField(max_length=32, verbose_name='Phone number', blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.CharField(max_length=16, verbose_name='Article')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'partner',
                'verbose_name_plural': 'partners',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='partner',
            field=models.ForeignKey(blank=True, to='users.Partner', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveIntegerField(verbose_name='Code')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create date')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'sms',
                'verbose_name_plural': 'sms',
            },
            bases=(models.Model,),
        ),
    ]
