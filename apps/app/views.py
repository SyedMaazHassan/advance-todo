# -*- encoding: utf-8 -*-

from django import template
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *


@login_required(login_url="/login/")
def index(request):
    all_tasks = Task.objects.all()
    if request.method == "POST":

        parent_task = request.POST.get('parent_task')
        due_date = request.POST.get('due_date')
        task_obj = Task(text=parent_task, due_date=due_date, is_parent=True, priority_index=1, created_by=request.user)
        task_obj.save()
        

        parent_id = request.POST.get('parent_id')
        filtered_parent = get_object_or_404(Task, id=parent_id)
        child_date = filtered_parent.due_date
        child_user = filtered_parent.created_by


        child_task_text = request.POST.get('child_text')
        child_task = Task(text = child_task_text, due_date = child_date, is_parent = False, priority_index=1,created_by = child_user )
        child_task.save()

        filtered_parent.child_task.add(child_task)
        return redirect('/')

        
    context = {
        'all_tasks': all_tasks,
    }
    for i in all_tasks:
        print(i.child_task.all())
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        segment, active_menu = get_segment( request )

        context['segment'] = segment
        context['active_menu'] = active_menu

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

# Helper - Extract current page name from request
def get_segment( request ):
    try:
        segment     = request.path.split('/')[-1]
        active_menu = None

        if segment == '' or segment == 'index.html':
            segment     = 'index'
            active_menu = 'dashboard'

        if segment.startswith('dashboard-'):
            active_menu = 'dashboard'

        return segment, active_menu

    except:
        return 'index', 'dashboard'




