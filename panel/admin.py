from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from panel.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone_namber', 'balance', 'created_at')
    fields = ('id', 'username', 'first_name', 'last_name', 'phone_namber', 'balance', 'created_at')

    exclude = ('data',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True


class AttachmentsInline(admin.TabularInline):
    model = Attachments

    exclude = ('file_id',)

    extra = 0


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'text', 'is_ok']
    readonly_fields = ['is_ok']
    inlines = [AttachmentsInline]
    
    
@admin.register(SupportHelp)
class SiteSettingsAdmin(admin.ModelAdmin):
    def get_object(self, request, object_id, from_field=None):
        return SupportHelp.load()

    def changelist_view(self, request, extra_context=None):
        obj = self.get_object(request, None)
        change_url = reverse(
            'admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name),
            args=[obj.pk]
        )
        return redirect(change_url)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True
