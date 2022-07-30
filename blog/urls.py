from django.urls import path
from . import views
from .views import home, PostDetail, PostCreate, PostUpdate, PostDelete, UserPost
urlpatterns = [
    path('', home.as_view(template_name = "blog/index.html"), name='blog-home'),
    path('/<str:username>/',UserPost.as_view(template_name="blog/user_posts.html") ,name='user-posts'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post/create/',PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post-update'),
    # path('post/<int:pk>/update/', views.UpdatePost, name='post-update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    # path('post/<int:pk>/delete/', views.DeletePost, name='post-delete'),
]