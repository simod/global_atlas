from django.contrib import admin
from .models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source, CollinsMap, MapHistory

class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}
    ordering = ['name']

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}

class RequesterAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}

class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',)}

class CountryAdmin(admin.ModelAdmin):
    filter_horizontal = ('countries',)
    search_fields = ['name',]
    ordering= ['name',]
    list_display = ('name', 'fips')

class MapRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'user',)
    search_fields = ['user__username',]

class MapAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'date')
    search_fields = ['title', 'id',]

class CollinsMapAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Theme, ThemeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(MapRequest, MapRequestAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Format)
admin.site.register(MapSize)
admin.site.register(Requester, RequesterAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(CollinsMap, CollinsMapAdmin)
admin.site.register(MapHistory)
