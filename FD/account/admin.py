from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'passwd',
        'gender',
        'age',
        'height',
        'weight',
        'reg_datetime',
        'gcode',
        'calorie'
    )

    list_display_links = (
        'id',
        'passwd',
        'gender',
        'age',
        'height',
        'weight',
        #'reg_datetime',
        'gcode',
        'calorie'
    )