from django.urls import path
from . import views, form_views
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('settings', views.settings, name='settings'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('signup', views.registration_view, name='signup'),
    path('change_password', form_views.password_change_view, name='change_password'),

    path('edit/basic_info', form_views.change_basic_user_data, name='modify_user'),


    # User URLS
    path('info/create_profile', form_views.create_user_profile_view, name='create_user_profile'),
    path('info/edit_profile', form_views.edit_user_profile, name='edit_user_profile'),
    path('info/add_education', form_views.add_education_view, name='add_education'),
    path('info/add_project', form_views.add_project_view, name='add_project'),
    path('info/add_certificate', form_views.add_certificate_view, name='add_certificate'),
    path('profile', views.dashboard, name='dashboard'),
    path('public_profile/<slug:username>', views.view_profile, name='public_profile'),

    # Urls for persons dashboard
    path(r'users/follow/', views.user_follow, name='user_follow'),
    # path(r'users/', views.recommended_user_list, name='user_list'),
    # path(r'users/<slug:username>', views.user_detail, name='user_detail'),

    # org URLS
    path('org_profile/edit', form_views.create_edit_company_profile, name='edit_company_profile'),
    path('manage_jobs', views.manage_jobs, name='manage_jobs'),
    path('manage_candidates/<slug:job_id>', views.manage_candidates, name='manage_candidates'),
    path('org_profile/<slug:id>', views.get_org_profile, name='get_org_profile'),
    path('post_job', views.post_job, name='post_job'),
    path('view_job/<slug:id>', views.view_job, name='view_job' )
]