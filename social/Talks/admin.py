from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Talks

# Unregister your models here:
admin.site.unregister(Group)
# admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Talks)
