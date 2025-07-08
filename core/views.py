from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Project, Issue, Company

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/test/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def test_tenant_view(request):
    # Handle superuser with no company
    if request.user.company:
        company_name = request.user.company.name
    else:
        company_name = "Superuser (All Companies)"
    
    projects = Project.objects.all()
    issues = Issue.objects.all()
    
    return JsonResponse({
        'user': request.user.username,
        'user_company': company_name,
        'projects_count': projects.count(),
        'issues_count': issues.count(),
        'projects': [p.title for p in projects],
        'issues': [i.title for i in issues],
    })