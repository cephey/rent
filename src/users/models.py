#coding:utf-8
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


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

    partner = models.ForeignKey('users.Partner', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = '{} {} {}'.format(self.first_name, self.last_name, self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


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

    class Meta:
        verbose_name = _('sms')
        verbose_name_plural = _('sms')

    def __unicode__(self):
        return u'Code {} for user {}'.format(self.code, self.user)


class Card(models.Model):

    article = models.CharField(_('Article'), max_length=16)
    user = models.ForeignKey('users.User')

    class Meta:
        verbose_name = _('cards')
        verbose_name_plural = _('card')

    def __unicode__(self):
        return u'Card № {} for user {}'.format(self.article, self.user)