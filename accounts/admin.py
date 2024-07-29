from django.contrib import admin
from .models import User
from allauth.socialaccount.models import SocialApp

#admin.site.register(SocialApp)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass