from django.urls import path
from .views import homepage,post_details,post_list, PostListView, post_share, post_list_by_month, PostCreateView, PostUpdateView, PostDeleteView
from . import views

app_name = 'blog'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('list/', post_list, name='post_list'),
    # path('list/', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_details, name='post_details'),
    path('<int:post_id>/share/',post_share, name='post_share'),
    path('profile/', views.profileEdit, name='profile'), 
    path('create/', PostCreateView.as_view(), name='postcreate'),
    # path('post_edit/', PostCreateView.as_view(), name='post_edit'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='postupdate'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='postdelete'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('archive/<int:year>/<int:month>/', post_list_by_month, name='list_by_month'),
    path('my_posts/', views.user_posts, name='my_posts'),
]