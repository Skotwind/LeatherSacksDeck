from django.contrib import admin

from .models import *


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Worker)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('title', 'warden')


@admin.register(UserInfo)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'sur_name')


@admin.register(HardSkill)
class HardSkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(SoftSkill)
class SoftSkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
