from django.contrib import admin
from blog.models import Category, Comment, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id",'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
admin.site.register(Comment)