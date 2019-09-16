from django.contrib import admin
from .models import Post, ImagePost, Action


class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'slug', 'created_on', 'updated_on')
    list_filter = ('author',)
    search_fields = ('author', 'title', 'content')


class ImagePostAdmin(admin.ModelAdmin):
    list_display = ('posted_by', 'slug', 'created_on',)
    list_filter = ('posted_by',)
    search_fields = ('posted_by', 'caption')


admin.site.register(Action, ActionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ImagePost, ImagePostAdmin)
