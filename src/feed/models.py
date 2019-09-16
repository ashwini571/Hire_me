from django.db import models
from accounts.models import Client
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        db_table = 'blog_post'
        app_label = 'feed'

    def __str__(self):
        return "{} - {}".format(self.author.username, self.title)

    def get_absolute_url(self):
        return reverse('feeds:blog_url',
                       kwargs={'identifier': self.slug})


class ImagePost(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    posted_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='image_posts')
    caption = models.TextField(max_length=1000, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image_posts/', blank=False, null=False)
    likes = models.ManyToManyField(Client, blank=True, null=True, related_name='likes')

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Image Post'
        verbose_name_plural = 'Image Posts'
        db_table = 'image_posts'
        app_label = 'feed'

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('feed:image_url', kwargs={'identifier': self.slug})

# Likes, Comments


class Action(models.Model):
    user = models.ForeignKey(Client, related_name='actions', db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=500)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'User Action'
        verbose_name_plural = 'User Actions'
        db_table = 'user_action'
        ordering = ('-created',)
        app_label = 'feed'

