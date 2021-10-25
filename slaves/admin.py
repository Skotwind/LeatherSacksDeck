from django.contrib import admin

from .models import *


@admin.register(Slave)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'sur_name', 'position', 'warden')


@admin.register(HardSkill)
class HardSkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(SoftSkill)
class SoftSkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
