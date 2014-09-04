#coding:utf-8
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.dispatch import receiver

from .managers import UserManager, SmsManager

from tastypie.models import ApiKey
import uuid


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), max_length=254, unique=True)

    first_name = models.CharField(_('first name'), max_length=64, blank=True)
    last_name = models.CharField(_('last name'), max_length=64, blank=True)
    patronymic = models.CharField(_('patronymic'), max_length=64, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    passport = models.CharField(_('Number of passport'),
                                max_length=32, blank=True)
    travel_passport = models.CharField(_('Travel passport number'),
                                       max_length=32, blank=True)
    drive_license = models.CharField(_('Driver\'s license number'),
                                     max_length=32, blank=True)

    photo = models.ImageField(blank=True, null=True)
    phone = models.CharField(_('Phone number'), max_length=32, blank=True)
    confirm = models.BooleanField(_('Phone confirm'), default=False)

    partner = models.ForeignKey('users.Partner', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = getattr(settings, 'USERNAME_FIELD', 'email')
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return reverse('users:update', kwargs={'pk': self.id})

    def get_full_name(self):
        full_name = '{} {} {}'.format(self.first_name, self.last_name, self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def thumb(self):
        if self.photo:
            return mark_safe(u'<img src="{}" height=40 />'.format(self.photo.url))
        return ''
    thumb.short_description = _('Thumbnail')


@receiver(post_save, sender=User)
def add_user_permission(sender, instance, **kwargs):
    ct1 = ContentType.objects.get(app_label="inventory", model="reserve")
    perm1 = Permission.objects.get(content_type=ct1, codename='add_reserve')
    ct2 = ContentType.objects.get(app_label="inventory", model="reserveea")
    perm2 = Permission.objects.get(content_type=ct2, codename='add_reserveea')
    instance.user_permissions.add(perm1, perm2)


@receiver(post_save, sender=User)
def create_user_api_key(sender, instance, **kwargs):
    if not ApiKey.objects.filter(user=instance).exists():
        key = ''.join(str(uuid.uuid4()).split('-'))
        ApiKey.objects.create(user=instance, key=key)


class Partner(models.Model):

    name = models.CharField(_('Name'), max_length=64, unique=True)

    class Meta:
        verbose_name = _('partner')
        verbose_name_plural = _('partners')

    def __unicode__(self):
        return self.name


class Sms(models.Model):

    user = models.ForeignKey('users.User')
    code = models.PositiveIntegerField(_('Code'))
    create_at = models.DateTimeField(_('Create date'), default=timezone.now)

    objects = SmsManager()

    class Meta:
        verbose_name = _('sms')
        verbose_name_plural = _('sms')
        ordering = ['-create_at']

    def __unicode__(self):
        return u'Code {} for user {}'.format(self.code, self.user)


class Card(models.Model):

    user = models.ForeignKey('users.User')
    article = models.CharField(u'Номер карты', max_length=16,
                               help_text=u'Сканируйте штрих код карты для '
                                         u'привязки ее к клиенту')

    class Meta:
        verbose_name = _('cards')
        verbose_name_plural = _('card')

    def __unicode__(self):
        return u'Card № {} for user {}'.format(self.article, self.user)
