from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number',
                    'position', 'date_of_birth', 'photo', 'date_of_start_working']
    raw_id_fields = ['user']
