from django.contrib import admin
from .models import Client, Project, UserProfile, Certifications, Education, JobApplication, OrgProfile, AppliedJobs , Contact


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'type')
    list_filter = ('type',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Info', {'fields': ('first_name', 'last_name', 'profile_image')}),
        ('User Type', {'fields': ('type',)}),
    )
    ordering = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ()


class OrgProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender')
    list_filter = ('gender',)
    search_fields = ('user', 'about')
    fieldsets = (
        ('User', {'fields': ('user', 'gender')}),
        ('Info', {'fields': ('about', 'resume', 'languages','skills')}),
    )
    filter_horizontal = ()


class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'degree', 'school', 'grade')
    search_fields = ('degree', 'school')
    fieldsets = (
        (None, {'fields': ('profile', 'degree')}),
        ('Info', {'fields': ('school', 'field_of_study', 'grade', 'description')}),
        ('Duration', {'fields': ('start_year', 'end_year', 'is_studying')})
    )
    filter_horizontal = ()


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'associated_with', 'project_URL')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {'fields': ('profile', 'name')}),
        ('Info', {'fields': ('associated_with', 'project_URL', 'description')}),
        ('Duration', {'fields': ('start_date', 'end_date', 'is_active')})
    )
    filter_horizontal = ()


class CertificationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'issuing_organisation',)
    search_fields = ('name', 'issuing_organisation')
    list_filter = ('issuing_organisation',)
    fieldsets = (
        (None, {'fields': ('profile', 'name')}),
        ('Info', {'fields': ('issuing_organisation', 'credential_ID', 'credential_URL')}),
        ('Duration', {'fields': ('issue_date',)})
    )
    filter_horizontal = ()


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'org', 'type')
    search_fields = ('title', 'org')


class AppliedJobadmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'status')


admin.site.register(Client, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Certifications, CertificationAdmin)
admin.site.register(OrgProfile, OrgProfileAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(AppliedJobs, AppliedJobadmin)
admin.site.register(Contact)