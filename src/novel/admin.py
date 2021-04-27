from django.contrib import admin

# Register your models here.
from novel.models import BookSource, Author, Category, Tag, Book, Chapter


@admin.register(BookSource)
class BookSourceAdmin(admin.ModelAdmin):
    # date_hierarchy = 'sequence'
    list_display = ('name', 'host')
    list_filter = ('name', 'host')
    # filter_horizontal = ('',)
    list_display_links = ('name', 'host')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name')
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name')
    list_filter = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name', 'channel')
    list_filter = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'ranking', 'words_count', 'state')
    list_filter = ('name', 'author', 'state')
    list_display_links = ('name', 'author')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name', 'book', 'source_id', 'next_chapter_id', 'prev_chapter_id')
    list_filter = ('name', 'book')
    list_display_links = ('name', 'book')

