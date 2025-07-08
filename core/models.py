from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import get_current_company

class TenantManager(models.Manager):
    """
    A Manager is Django's interface for database operations. It's the object that provides methods like .all(), .filter(), .get(), etc.
    Every Model Has a Manager

    class Issue(models.Model):
        title = models.CharField(max_length=200)
    
        # Django automatically creates this behind the scenes:
        # objects = models.Manager()
    ######################################
    What Does a Manager Do?
        Issue.objects.all()      # Manager method
        Issue.objects.filter()   # Manager method  
        Issue.objects.get()      # Manager method
        Issue.objects.create()   # Manager method
    ######################################
    The Manager is responsible for:
      -Building database queries
      -Returning QuerySets
      -Handling bulk operations
    Model = describes your data structure
    Manager = provides methods to query that data
    """
    def get_queryset(self):
        current_company = get_current_company()
        if current_company:
            return super().get_queryset().filter(company=current_company)
        return super().get_queryset()
    def all(self):
        return self.get_queryset().all()

class Company(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True) # This is so superusers don't need a company
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('manager', 'Manager'), 
        ('developer', 'Developer'),
    ], default='developer')

class Project(models.Model):
    title = models.CharField(max_length=200)  # CharField for titles
    description = models.TextField()  # TextField for longer text
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, blank=True)
    
    objects = TenantManager()  # Apply tenant filtering

class Issue(models.Model):
    title = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # For fast queries
    
    objects = TenantManager()  # Apply tenant filtering



