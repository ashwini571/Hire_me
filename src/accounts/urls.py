from django.urls import path
from . import views, form_views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('settings', views.settings,name='settings'),
    path('org_profile/<slug:id>', views.get_org_profile, name='get_org_profile'),
    path('signup', views.registration_view, name='signup'),
    path('change_password', form_views.password_change_view, name='change_password'),

    path('edit/basic_info', form_views.change_basic_user_data, name='modify_user'),

    # FormURLS
    path('info/create_profile', form_views.create_user_profile_view, name='create_user_profile'),
    path('info/add_education', form_views.add_education_view, name='add_education'),
    path('info/add_project', form_views.add_project_view, name='add_project'),
    path('info/add_certificate', form_views.add_certificate_view, name='add_certificate'),
]