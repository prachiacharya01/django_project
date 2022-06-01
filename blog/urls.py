from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import PostListView, PostDetailView, PostCreateView ,PostUpdateView,PostDeleteView,desc1
# from blog import admin

from rest_framework import routers
from .views import PostSerialzerView,commentSerializerView

router = routers.DefaultRouter()
router.register('postserial', PostSerialzerView, basename='postserial')
router.register("comment",commentSerializerView,basename= "comment")
# urlpatterns = router.urls

urlpatterns = [
    # path('', views.home, name ='blog-home'),
    path('',PostListView.as_view(template_name = 'blog/home.html'),name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(template_name='blog/post_detail.html'),name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name = "post-delete"),
    path('donate/', views.donate,name = "post-donate"),
    path('about/', views.about, name ='blog-about'),
    path('login/', auth_views.LoginView.as_view(template_name = 'blog/login.html'), name='blog-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'blog/logout.html'),name='blog-logout'),  
    path('searchbar/',views.search,name='searchbar'),
    path('desc/<int:pk>/',desc1.as_view(template_name = 'blog/desc.html'),name='desc'),
    # path('like/<int:pk>/',views.LikeView,name='blog-like'),
    # path('like/<int:pk>/',views.DisLikeView,name='blog-dislike')
    # path('a/',views.desc,name="a")
    # path('register/',views.register,name='blog-register')

    # serializers
    path("s1/",views.hello.as_view(), name="s1"),
    path('r', include(router.urls)),
    path('hello/', views.HelloView.as_view(), name ='hello'),
  
    # pdf generator
    path("pdf/",views.gen_pdf,name="pdf")
]
