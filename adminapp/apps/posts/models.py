from django.db import models
from django.utils.text import slugify

from apps.users.models import User
from apps.common.models import TimestampedModel


class Post(TimestampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", related_name="posts")
    category = models.ForeignKey("Category", related_name="posts", on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(TimestampedModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'
        ordering = ['-created_at']
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Category(TimestampedModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
