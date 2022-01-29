import csv
from datetime import datetime, timedelta

from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import AdminSite
from django.contrib.auth import get_permission_codename
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import ngettext

from blog.models import Post


class MyAdminSite(AdminSite):
    # Disable View on Site link on admin page
    site_url = None


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


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', ]
        exclude = ['publish']


class PostAdmin(admin.ModelAdmin):
    # def view_on_site(self, obj):
    #     url = reverse('blog-detail', kwargs={'slug': obj.slug})
    #     return 'https://example.com' + url

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

    @admin.action(permissions=['change', 'publish'], description='Mark selected blog as published', )
    def publish_blog(self, request, queryset):
        updated = queryset.count()
        try:
            queryset.update(publish=timezone.now() - timedelta(days=1), status='published')
            self.message_user(request, ngettext(
                '%d blog was published successfully.',
                '%d blogs were published successfully.',
                updated,
            ) % updated, messages.SUCCESS)

        except:
            self.message_user(request, ngettext(
                '%d blog was not published successfully.',
                '%d blogs were not published successfully.',
                updated,
            ) % updated, messages.ERROR)

    def has_publish_permission(self, request):
        """Does the user have the blog publish permission?"""
        opts = self.opts
        codename = get_permission_codename('publish', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

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
    search_fields = ('title', 'author', 'author__username', 'status',)
    search_help_text = "Search for title, author, and status."
    show_full_result_count = False
    list_filter = (BlogStatusListFilter, 'author',)
    actions = [export_to_csv, make_draft_using_secondary_page, publish_blog, ]

    # fields = ('title', 'body',)
    fieldsets = [
        ("Basic", {'fields': ['title', 'body', 'status', ], "description": "Basic information"}),
        ("Author", {'fields': ['author', 'published_by', ], "description": "Author information"}),
        ("Date", {
            'classes': ('wide',),
            'fields': ['publish', ]
        }),
    ]
    # form = BlogForm
    list_editable = ('title',)
    prepopulated_fields = {"body": ("title",)}
    autocomplete_fields = ['author', ]
    save_as_continue = True
    save_as = True
    save_on_top = True
    export_to_csv.short_description = 'Export to CSV'
    # actions = None
    view_on_site = False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    @admin.display(description='Name', empty_value='N/A')
    def author_full_name(self, obj):
        return "%s %s" % (obj.author.first_name, obj.author.last_name)

    def marked_blog_status(self, obj):
        if obj.status == "draft":
            return format_html('<span style="color: #{};">{}</span>', "F6CC0A", obj.status.title(), )
        return format_html('<span style="color: #{};">{}</span>', "12B873", obj.status.title(), )


admin.site.register(Post, PostAdmin)
# admin.site.disable_action('delete_selected')
