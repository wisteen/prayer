from django.contrib import admin
from .models import Planet, MagicalHour, WeekdayStart

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ("order_index", "name", "angel")
    list_editable = ("name", "angel")
    ordering = ("order_index",)

@admin.register(MagicalHour)
class MagicalHourAdmin(admin.ModelAdmin):
    list_display = ("index", "name")
    list_editable = ("name",)
    ordering = ("index",)

@admin.register(WeekdayStart)
class WeekdayStartAdmin(admin.ModelAdmin):
    list_display = ("day", "get_day_display", "planet")
    list_select_related = ("planet",)
    ordering = ("day",)
