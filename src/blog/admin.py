from django.contrib import admin

# Register your models here.


from blog.models import Tag, Article, Category, Links, Carousels, BlogSettings


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_time'
    list_display = ('title', 'category', 'author', 'date_time', 'view')
    list_filter = ('category', 'author')
    filter_horizontal = ('tag',)
    list_display_links = ('title', 'date_time')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name', 'link', 'description', 'is_enable')
    list_filter = ('name', 'link')
    list_display_links = ('name', 'link', 'description')


@admin.register(Carousels)
class CarouselsAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name', 'link', 'is_enable')
    list_filter = ('name', 'link')
    list_display_links = ('name', 'link')


@admin.register(BlogSettings)
class BlogSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'seo_description', 'keywords')
    list_filter = ('name', 'description')
    list_display_links = ('name', 'description')
    

