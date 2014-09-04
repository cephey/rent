#coding:utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User, Partner, Sms, Card


@admin.register(User)
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
        (_('Private'), {'fields': ('photo', 'phone', 'confirm', 'partner')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('get_display','thumb', 'first_name', 'last_name',
                    'patronymic', 'is_staff', 'is_active', 'confirm')
    search_fields = ('email', 'first_name', 'last_name', 'patronymic')
    ordering = ('email',)

    def get_display(self, obj):
        return obj.email if obj.email else obj.id
    get_display.short_description = 'email'


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    pass


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass
