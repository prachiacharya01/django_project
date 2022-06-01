from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name = 'register'),
    path('profile/', user_views.profile, name = 'profile'),
    path('', include('blog.urls')),
    # dedbug
    path('__debug__/', include('debug_toolbar.urls')),

    # serializers
    path("g1/<int:pk>/",user_views.ProfileSerializerView.as_view(),name="g1"),

    # celery
    path("celery/",user_views.test1, name = "celery")

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Blog Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Portal"
   
urlpatterns += [
    path('api/token/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),
]