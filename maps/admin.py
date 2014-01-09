from django.contrib import admin
from .models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source

class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}

class RequesterAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}

class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}

class CountryAdmin(admin.ModelAdmin):
    filter_horizontal = ('countries',)

admin.site.register(Theme, ThemeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Map)
admin.site.register(MapRequest)
admin.site.register(Country, CountryAdmin)
admin.site.register(Format)
admin.site.register(MapSize)
admin.site.register(Requester, RequesterAdmin)
admin.site.register(Source, SourceAdmin)