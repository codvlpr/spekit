from django.contrib import admin
from . import models


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TopicItem)
class TopicItemAdmin(admin.ModelAdmin):
    pass
