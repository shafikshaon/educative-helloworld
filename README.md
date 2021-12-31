# educative-helloworld

## Show list of fields
You need to set `list_display` to control which fields you want to show in the admin interface.
Let's say you want to show the following fields in the admin interface
- id
- title
- author
- created
- publish

Write the following code snippet to display the list of fields in the admin interface.

"`python
from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'created', 'publish',
    )


admin.site.register(Post, PostAdmin)

```

You will see UI like following
![](/api/collection/5741532031221760/6679588215717888/page/4667729029627904/image/5125082447347712?page_type=collection_lesson)

If you don't set `list_display`, the admin site will display a single column that shows each object's `__str__()` representation.


## Adding custom fields

Let's say you want to show the author's full name, but there is no direct model attribute to show the author's full name. So, it would be best if you wrote a custom admin display attribute to display in the admin interface.

```python
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author_full_name', 'created', 'publish',
    )

    @admin.display(description='Name', empty_value='N/A')
    def author_full_name(self, obj):
        return "%s %s" % (obj.author.first_name, obj.author.last_name)
```

The `description` will show as table header, and `empty_value` shows `N/A` if not value found for that author.


You will see UI like following after writing the custom `author_full_name` method.
![](/api/collection/5741532031221760/6679588215717888/page/4667729029627904/image/6400559355002880?page_type=collection_lesson)

> If the field is a `ForeignKey`, Django will display the `__str__()` of the related object.

> `ManyToManyField` fields aren't supported; you need to write a custom method if you need this.

> If the field is a `BooleanField`, Django will display a pretty "yes", "no", or "unknown" icon instead of **True**, **False**, or **None**.

## format_html
You can also use the `format_html` instruction to return HTML.
If you want to display blog status in color, you can write a custom method that returns `format_html`.

```python
    def marked_blog_status(self, obj):
        if obj.status == "draft":
            return format_html('<span style="color: #{};">{}</span>', "F6CC0A", obj.status.title(), )
        return format_html('<span style="color: #{};">{}</span>', "12B873", obj.status.title(), )
```

You will see UI like following after writing the custom `marked_blog_status` method.
![](/api/collection/5741532031221760/6679588215717888/page/4667729029627904/image/5092567984635904?page_type=collection_lesson)

## empty_value_display
If a field value is `None`, the Django admin interface is shown as `-`. But, you can override this value.

```python
class PostAdmin(admin.ModelAdmin):
    empty_value_display = 'unknown'
```


## list_display_links
If you want any field link to the change page, use **list_display_links**. 

By default, the change list page will link the first column – the first field specified in **list_display** – to the change page for each item. 

You can set it to **None** to get no links at all.

```python
class PostAdmin(admin.ModelAdmin):
    list_display_links = None
```

You can specify one or many fields. As long as the fields appear in **list_display**, make sure to define the same field in **list_display**. 

In this example, the **id** and **author** fields will be linked on the change list page:

```python
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'marked_blog_status', 'author', 'created', 'publish', 'views_count', 'is_recently_created',
    )
    list_display_links = ('id', 'author',)
```


## list_max_show_all
To limit how many items appear when the user clicks "Show all", you need to `list_max_show_all `. The default value is 200. The "Show all" is only shown if the number of items count is less than equal to the `list_max_show_all` setting. For example;


```python
class PostAdmin(admin.ModelAdmin):
    list_max_show_all = 500
```

## list_per_page
Set `list_per_page` to control how many items appear on each paginated admin change list page. The default value is 100. For example:

```python
class PostAdmin(admin.ModelAdmin):
    list_per_page = 200
```


## list_select_related
To save multiple database queries, you can set ForeignKey fields in `list_select_related`. For example:

```python
class PostAdmin(admin.ModelAdmin):
    list_select_related = ('author',)
```

## ordering
Set ordering to specify how lists of objects should be ordered. For example:

```python
class PostAdmin(admin.ModelAdmin):
    ordering = ('-created', 'publish',)
```


## preserve_filters
By default, applied filters are preserved on the list view after creating, editing, or deleting an object. You can have filters cleared by setting this attribute to **False**.


## date_hierarchy
Set **date_hierarchy** to the name of a **DateField** or DateTimeField in your model, and the change list page will include a date-based drill-down navigation by that field. For example:

```python
class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish'
```





## Live demo
Now you can see all the necessary steps to register Post app. Execute the application by clicking on the run button. The default credentials are:

**Username:** educative

**Password:** p@ss1234
