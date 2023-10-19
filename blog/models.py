from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf import settings
from ckeditor.fields import RichTextField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    
    date_of_birth = models.DateTimeField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to = 'users/%Y/%m/%d/',
                                        blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'
    

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    
    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.title


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = RichTextField()
    authors_comment = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.ForeignKey(Category, related_name='tag',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('blog:post_details',
                        args=[self.publish.year,
                        self.publish.month,
                        self.publish.day, self.slug])
        
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'

  
class IntroPost(models.Model):
    intro_text = models.TextField(max_length=250)
    title = models.CharField(max_length=200)
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='introPost')
    active = models.BooleanField(default=True)
