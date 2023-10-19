from django import template
from blog.models import Post
from django.db.models import Count
from django.contrib.auth.models import User


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

# @register.inclusion_tag('blog/post/latest_posts.html')
# def show_latest_posts(count=5):
#     latest_posts = Post.published.order_by('-publish'[:count])
#     return {'latest_posts': latest_posts}

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.simple_tag
def get_most_viewed_posts(count=3):
    return Post.published.order_by('-views')[:count]

# @register.inclusion_tag('blog/user/user_posts.html')
# def user_posts(user):
#     published_posts = Post.objects.filter(author=user, status='published')
#     draft_posts = Post.objects.filter(author=user, status='draft')
#     return {'published_posts': published_posts, 'draft_posts': draft_posts}