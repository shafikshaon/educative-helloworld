import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
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
    def make_draft_using_secondary_page(self, request, queryset):
        if 'apply' in request.POST:
            # # Perform our update action:
            queryset.update(status='draft')
            # Redirect to our admin view after our update has
            # completed with a nice little info message saying
            # our models have been updated:
            self.message_user(request,
                              "Changed to DRAFT on {} post".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'admin/make_draft.html', context={'posts': queryset})

    def export_to_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; \
            filename={}.csv'.format(opts.verbose_name)
        writer = csv.writer(response)
        fields = [field for field in opts.get_fields()
                  if not field.many_to_many and not field.one_to_many]
        # Write a first row with header information
        writer.writerow([field.verbose_name for field in fields])
        # Write data rows
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y %H:%M:%S')
                data_row.append(value)
            writer.writerow(data_row)
        return response

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
    actions = [export_to_csv, make_draft_using_secondary_page, ]

    @admin.display(description='Name', empty_value='N/A')
    def author_full_name(self, obj):
        return "%s %s" % (obj.author.first_name, obj.author.last_name)

    def marked_blog_status(self, obj):
        if obj.status == "draft":
            return format_html('<span style="color: #{};">{}</span>', "F6CC0A", obj.status.title(), )
        return format_html('<span style="color: #{};">{}</span>', "12B873", obj.status.title(), )


admin.site.register(Post, PostAdmin)
