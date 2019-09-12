from django.urls import path
from . import views
from django.conf.urls.static import static
from HireMe import settings

app_name = 'feeds'

urlpatterns = [
    path(r'posts/<slug:identifier>', views.blog_view, name='blog_url'),
    path(r'images/<slug:identifier>', views.image_view, name='image_url'),
    path(r'add_post/', views.create_post_view, name='create_post'),
    path(r'add_image_post/', views.create_image_post_view, name='add_image_post'),
    path(r'404', views.error404, name='404'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)