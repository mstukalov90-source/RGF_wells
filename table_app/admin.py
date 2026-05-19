from django.contrib import admin

from .models import Well


@admin.register(Well)
class WellAdmin(admin.ModelAdmin):
    list_display = ('name_mst', 'n_skv', 'tip_skv', 'region', 'id_xy')
    search_fields = ('name_mst', 'n_skv', 'id_xy', 'lic', 'strat')
    list_filter = ('tip_skv', 'region')
