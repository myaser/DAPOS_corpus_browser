from django.contrib import admin
from indexer.models import Tweet, MainIndex, AuxiliaryIndex


class TweetAdmin(admin.ModelAdmin):
    detail_title = 'tweet detail'
    list_page_title = 'tweets'
    list_display = ('created_at', 'tweet_id', 'tweet_text', 'hash_tags', 'mentions')
    _fields = Tweet._meta.get_all_field_names()
    _fields.remove('posting')
    readonly_fields = _fields
    ordering = ['created_at']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(TweetAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class IndexAdmin(admin.ModelAdmin):
    detail_title = 'index details'
    list_page_title = 'index list'
    list_display = ('token', 'postings')
    readonly_fields = MainIndex._meta.get_all_field_names()
    ordering = ['token']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(IndexAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Tweet, TweetAdmin)
admin.site.register(MainIndex, IndexAdmin)
admin.site.register(AuxiliaryIndex, IndexAdmin)
