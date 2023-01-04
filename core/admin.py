from django.contrib import admin
from .models import PostBlog, PostNews, Comments, Review

# Register your models here.

@admin.register(PostBlog)
class PostBlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'id', 'created_at', 'views')
    list_filter = ('favourite', 'tags', 'created_at')


@admin.register(PostNews)
class PostNewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',),}
    list_display = ('title', 'id')
    list_filter = ('created_at',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

""" @admin.register(FavouritePost)
class FavouritePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post','id')
    list_filter = ('user', 'post') """

#admin.site.register(PostBlog, PostBlogAdmin)
#admin.site.register(FavouritePost, FavouritePostAdmin)