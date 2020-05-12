from django.contrib import admin

# Register your models here.
from .models import Author, Category, Post, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)

class BlogCommentsInline(admin.TabularInline):
    """Used to show 'existing' blog comments inline below associated blogs"""
    model = Comment
    max_num=0

@admin.register(Post)

class BlogAdmin(admin.ModelAdmin):
    """Administration object for Blog models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields), grouping the date fields horizontally
     - adds inline addition of blog comments in blog view (inlines)
    """
    list_display = ('title', 'author', 'post_date')
    inlines = [BlogCommentsInline]