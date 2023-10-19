from django.shortcuts import render,get_object_or_404, redirect
from .models import Post, IntroPost
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from.models import Profile
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from . forms import ProfileEdit, UserEditForm, PostForm
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import datetime

# from.models import Profile

# Create your views here.

@login_required(login_url='login')
def homepage(request, tag_slug=None):
    posts =Post.published.all()
    months = Post.objects.filter(status='published').annotate(month=TruncMonth('publish')).values('month').distinct().order_by('-month')

    # intro_posts = IntroPost
    tag = None
    tag_list = Tag.objects.all()
    tag_items = []
    for tag_item in tag_list:
        tag_items.append(tag_item)
        print(tag_item)
    print(tag_items)
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag]) 
    return render(request, 'blog/home.html', {'tag':tag,
                                              'tag_list':tag_list,
                                              'posts':posts,
                                              'months':months,})

@login_required(login_url='login')
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    tag_list = Tag.objects.all()
    
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
        
    paginator = Paginator(object_list, 6) # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'page':page,
                                                   'tag':tag,
                                                   'tag_list':tag_list,})

@login_required(login_url='login')
def post_details(request, year, month, day, slug):
    posts = get_object_or_404(Post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)
    
    if posts == EmptyPage:
        return homepage
    
    tag = None
    tag_list = Tag.objects.all()
    
    comments = posts.comments.filter(active=True)
    
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = posts
            new_comment.save()
            
            # Redirect user back to the post_details page
            
            # latest_post = Post.objects.filter(status='published').latest('publish')
            # year, month, day = latest_post.publish.year, latest_post.publish.month, latest_post.publish.day,
            # latest_post_slug = latest_post.slug
            return redirect('blog:post_details', year=posts.publish.year,
                            month=posts.publish.month, day=posts.publish.day,
                            slug=posts.slug)
          
    else:
        comment_form = CommentForm()
    
    #List of similar posts
    post_tags_ids = posts.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)
    
    posts.views += 1
    posts.save()
    
    context = {
            'posts': posts,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts':similar_posts,
            'tag_list': tag_list,}
    
    return render(request, 'blog/post/details.html', context)

class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    
@login_required(login_url='login')   
def post_share(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id, status='published')
    
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{user} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{user}'s comments: {cd['comments']}"
            send_mail(subject, message, user.email, [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
    
@login_required(login_url='login')
def post_list_by_month(request, year, month):
    selected_month = datetime.strptime(f'{year}-{month}', '%Y-%m')
    view = "post_list_by_month"
    posts = Post.objects.filter(status='published', publish__year=year, publish__month=month).order_by('-publish')
    paginator = Paginator(posts, 3) # Show 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'posts': posts,
        'page': page,
        'year': year,
        'month': month,
        'view' : view,
        'selected_month': selected_month,
    }
    return render(request, 'blog/post/list.html', context)

@login_required(login_url='login')
def profileEdit(request):

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
        messages.warning(request, 'Profile does not exist')

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEdit(instance=request.user.profile,
                                   data=request.POST,
                                   files=request.FILES)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            # print(request.POST['date_of_birth'])
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEdit(instance=request.user.profile)
    
    context = {'user_form':user_form, 'profile_form':profile_form, 'profile':profile }

    return render(request, 'user/profile.html', context)

# @login_required
# def PostCreateView(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('blog:post_details', year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post/create.html', {'form': form})


# @login_required
# def PostUpdateView(request, year, month, day, slug):
#     post = get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month, publish__day=day, author=request.user)
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('blog:post_details', year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post/edit.html', {'form': form})

class PostCreateView( CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        if 'title' in self.request.GET:
            initial['title'] = self.request.GET['title']
            initial['slug'] = slugify(self.request.GET['title'])
        return initial

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:my_posts')

    # fields = ['title',  'slug', 'body', 'image', 'tags', 'author', 'status']
    template_name = 'blog/post/post_form.html'

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:my_posts')
    template_name = 'blog/post/post_confirm_delete.html'


@login_required(login_url='login')   
def user_posts(request):
    user = request.user
    published_posts = Post.objects.filter(author=user, status='published')
    draft_posts = Post.objects.filter(author=user, status='draft')
    return render(request, 'user/user_posts.html', {'published_posts': published_posts, 'draft_posts': draft_posts})