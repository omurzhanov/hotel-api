from django.contrib import admin
from .models import *

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    max_num = 10
    min_num = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline, ]


admin.site.register(Rating)