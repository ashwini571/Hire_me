from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from taggit.managers import TaggableManager
# from location_field.models.spatial import LocationField


class IndividualManager(models.Manager):
    def get_queryset(self):
        return super(IndividualManager, self).get_queryset().filter(type='user')


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super(CompanyManager, self).get_queryset().filter(type='org')


class Client(AbstractUser):

    TYPES = (
        ('user', 'User'),
        ('org', 'Organization')
    )

    profile_image = models.ImageField(null=True, blank=True, upload_to='users/')
    type = models.CharField(max_length=4, choices=TYPES, default='user')
    objects = UserManager()
    users = IndividualManager()
    companies = CompanyManager()

    @property
    def image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return r"https://res.cloudinary.com/dz2bsme0a/image/upload/v1548468434/user.png"

    def __str__(self):
        return self.username

    def is_individual(self):
        return self.type == 'user'

    def is_organisation(self):
        return self.type == 'org'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        base_manager_name = 'objects'
        default_manager_name = 'objects'
        db_table = 'clients'


class UserProfile(models.Model):
    SEXES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Others')
    )

    user = models.OneToOneField(Client, on_delete=models.CASCADE,related_name='profile')
    gender = models.CharField(choices=SEXES, max_length=1, blank=True, null=True)
    skills = TaggableManager()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    about = models.TextField(max_length=3000, blank=True, null=True)
    languages = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        db_table = 'user_profiles'


class OrgProfile(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='profile_org')
    verification = models.BooleanField(default=True)
    about = models.TextField(blank=False,null=False,max_length=10000)
    mis_vis = models.TextField(blank=False,null=False,max_length=10000)
    why = models.TextField(blank=False,null=False,max_length=10000)
    area_of_work = TaggableManager()
    teams = models.CharField(blank=False, null=False, max_length=100)
    # location = p

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Org Profile'
        verbose_name_plural = 'Org Profiles'
        db_table = 'org_profiles'


class Education(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='education')
    school = models.CharField(blank=False, null=False, max_length=100)
    degree = models.CharField(blank=False, null=False, max_length=100)
    field_of_study = models.CharField(blank=True, null=True, max_length=100)
    start_year = models.DateField()
    end_year = models.DateField()
    is_studying = models.BooleanField(default=True)
    grade = models.CharField(max_length=10, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.profile.user.username, self.school)

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'
        db_table = 'user_educations'


class Certifications(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(blank=False, null=False, max_length=100)
    issuing_organisation = models.CharField(blank=False, null=False, max_length=100)
    issue_date = models.DateField()
    credential_ID = models.CharField(blank=False, null=False, max_length=100)
    credential_URL = models.URLField(blank=False, null=False, max_length=100)

    def __str__(self):
        return "{}-{}".format(self.profile.user.username, self.name)

    class Meta:
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
        db_table = 'user_certifications'


class Project(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(blank=False, null=False, max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    associated_with = models.CharField(max_length=100)
    project_URL = models.URLField(blank=False, max_length=100)
    description = models.TextField(blank=False)

    def __str__(self):
        return "{}-{}".format(self.profile.user.username, self.name)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        db_table = 'user_projects'


class JobApplication(models.Model):
    choices = (
        ('f', 'Full-Time'),
        ('i', 'Intern'),
    )
    org = models.ForeignKey(OrgProfile, on_delete=models.CASCADE, related_name='JobApplication')
    title = models.CharField(blank=False, null=False, max_length=100)
    salary = models.CharField(blank=False, null=False, max_length=100)
    type = models.CharField(max_length=2, choices=choices, default='f')
    descr = models.TextField(blank=False)
    location = models.CharField(blank=False, null=False, max_length=100)

    class Meta:
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'

    def __str__(self):
        return "{}-{}".format(self.org.user.username, self.title)

