from django.contrib import admin
from django.utils.html import format_html

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    empty_value_display = '...'
    # list_display_links = None
    list_display_links = ('id', 'author',)
    list_max_show_all = 500
    list_per_page = 5
    list_select_related = ('author',)
    ordering = ('-created', 'publish',)
    date_hierarchy = 'publish'
    list_display = (
        'id', 'title', 'author_full_name', 'author', 'created', 'publish', 'marked_blog_status', 'summery'
    )

    @admin.display(description='Name', empty_value='N/A')
    def author_full_name(self, obj):
        return "%s %s" % (obj.author.first_name, obj.author.last_name)

    def marked_blog_status(self, obj):
        if obj.status == "draft":
            return format_html('<span style="color: #{};">{}</span>', "F6CC0A", obj.status.title(), )
        return format_html('<span style="color: #{};">{}</span>', "12B873", obj.status.title(), )


admin.site.register(Post, PostAdmin)
