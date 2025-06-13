from django.contrib import admin
from blog.models import Category, Comment, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id",'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id",'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Comment)