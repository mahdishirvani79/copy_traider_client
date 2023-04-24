from django.contrib import admin
from copy_traider.models import Symbols, OpenOrders
# Register your models here.


class SymbolsAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Symbols, SymbolsAdmin)


# class DemSupAdmin(admin.ModelAdmin):
#     list_display = ["symbol", "zoneStart"]


# admin.site.register(DemSupZones, DemSupAdmin)


class OpenOrderAdmin(admin.ModelAdmin):
    list_display = ["symbol", "active"]


admin.site.register(OpenOrders, OpenOrderAdmin)


# class OpenPositionsAdmin(admin.ModelAdmin):
#     list_display = ["ticket", "active"]


# admin.site.register(OpenPositions, OpenPositionsAdmin)
