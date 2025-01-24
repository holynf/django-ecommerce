from django.db import models
from django.urls import reverse
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    slug = models.SlugField(max_length=255,unique=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User,related_name="post_comment_user", on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} on '{self.post}'"