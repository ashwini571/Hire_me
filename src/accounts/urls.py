from django.urls import path
from . import views, form_views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.registration_view, name='signup'),

    # FormURLS
    path('info/create_profile', form_views.create_user_profile_view, name='create_user_profile'),
    path('info/add_education', form_views.add_education_view, name='add_education'),
    path('info/add_project', form_views.add_project_view, name='add_project'),
    path('info/add_certificate', form_views.add_certificate_view, name='add_certificate'),
]