from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Project, Issue, Company

@login_required
def test_tenant_view(request):
    # These should automatically filter by the current user's company
    projects = Project.objects.all()
    issues = Issue.objects.all()
    
    return JsonResponse({
        'user_company': request.user.company.name,
        'projects_count': projects.count(),
        'issues_count': issues.count(),
        'projects': [p.title for p in projects],
    })