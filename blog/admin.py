from django.contrib import admin
from django.utils.html import format_html

from blog.models import Post


class BlogStatusListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Blog status'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Published', ('Published blog')),
            ('Unpublished', ('Unpublished blog')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'Published':
            return queryset.filter(status='published')
        if self.value() == 'Unpublished':
            return queryset.filter(status='draft')


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
    search_fields = ('title', 'author__username', 'status',)
    search_help_text = "Search for title, author, and status."
    show_full_result_count = False
    list_filter = (BlogStatusListFilter, 'author',)

    @admin.display(description='Name', empty_value='N/A')
    def author_full_name(self, obj):
        return "%s %s" % (obj.author.first_name, obj.author.last_name)

    def marked_blog_status(self, obj):
        if obj.status == "draft":
            return format_html('<span style="color: #{};">{}</span>', "F6CC0A", obj.status.title(), )
        return format_html('<span style="color: #{};">{}</span>', "12B873", obj.status.title(), )


admin.site.register(Post, PostAdmin)
