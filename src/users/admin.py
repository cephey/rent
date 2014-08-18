#coding:utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Partner, Sms, Card
from forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'patronymic')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Documents'), {'fields': ('passport', 'travel_passport',
                                     'drive_license')}),
        (_('Private'), {'fields': ('photo', 'phone', 'partner')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'patronymic', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'patronymic')
    ordering = ('email',)

admin.site.register(User, UserAdmin)


class PartnerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Partner, PartnerAdmin)


class SmsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sms, SmsAdmin)


class CardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Card, CardAdmin)