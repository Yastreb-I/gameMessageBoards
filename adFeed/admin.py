from django.contrib import admin
from .models import Advertisement, Reaction


class AdvertisementAdmin(admin.ModelAdmin):
    readonly_fields = ['dateCreation']
    list_display = ['head', 'preview', 'category', 'author', 'dateCreation']


admin.site.register(Advertisement, AdvertisementAdmin)


class ReactionAdmin(admin.ModelAdmin):
    readonly_fields = ['dateCreation']
    list_display = ['ads', 'user', 'text', 'status', 'dateCreation']


admin.site.register(Reaction, ReactionAdmin)


