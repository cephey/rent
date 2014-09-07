#coding:utf-8
from django.contrib.auth.models import BaseUserManager
from django.shortcuts import get_object_or_404
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db import models

import random
import logging

logger = logging.getLogger('sms')


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff,
                     is_superuser, **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def confirm(self, id, code):
        Sms = get_model('users', 'Sms')
        if Sms.objects.filter(user__id=id, code=code).exists():
            Sms.objects.filter(user__id=id, code=code).delete()
            self.filter(id=id).update(confirm=True)

    def ready_for_pay(self):
        Reserve = get_model('inventory', 'Reserve')
        return [{'f': r.user.get_full_name(), 'r': r.id,
                 'u': reverse('inventory:contract', kwargs={'pk': r.id})}
                for r in Reserve.objects.filter(status=Reserve.RESERVE)
                    .select_related('user')]


class SmsManager(models.Manager):

    def send_sms_code(self, user_id):
        user = get_object_or_404(get_model('users', 'User'), pk=user_id)
        code = random.randint(100000, 999999)
        self.create(user=user, code=code)
        # SEND CODE TO PHONE
        logger.info('Code is {}'.format(code))
