from django.db import models
from accounts.models import Client
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Comment(models.Model):
    limit = models.Q(app_label='feed', model='post') | models.Q(app_label='feed', model='imagepost')
    user = models.ForeignKey(Client, related_name='comments', db_index=True, on_delete=models.CASCADE)
    body = models.TextField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, blank=False, on_delete=models.CASCADE, limit_choices_to=limit,
                                     related_name='child_comment')
    object_id = models.PositiveIntegerField(blank=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        db_table = 'comments'
        ordering = ('created',)
        app_label = 'feed'

    def __str__(self):
        return "{} commented at {}".format(self.user.username, str(self.created))


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    likes = models.ManyToManyField(Client, blank=True, related_name='post_likes')
    created_on = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(Comment, blank=True, null=True)

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
    likes = models.ManyToManyField(Client, blank=True, related_name='likes')
    comments = GenericRelation(Comment, blank=True, null=True)

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
    TYPES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('new_img', 'Added Image'),
        ('new_post', 'Added Post'),
        ('new_job', 'Added Job'),
        ('job_response', 'Responded to Job'),
        ('applied_to_job', 'Applied for Job'),
    )
    user = models.ForeignKey(Client, related_name='actions', db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=500)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    type = models.CharField(choices=TYPES, null=True, blank=True, max_length=15)

    class Meta:
        verbose_name = 'User Action'
        verbose_name_plural = 'User Actions'
        db_table = 'user_action'
        ordering = ('-created',)
        app_label = 'feed'

    def __str__(self):
        return self.verb
