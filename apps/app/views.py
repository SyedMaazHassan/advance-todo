# -*- encoding: utf-8 -*-

from django import template
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.utils import timezone
import json

@login_required(login_url="/login/")
def create_task(request):
    if request.method == "POST":
        parent_task = request.POST.get('parent_task')
        due_date = request.POST.get('due_date')

        all_current_tasks = Task.objects.filter(general_status = due_date, created_by = request.user, status=0, is_parent=True).count()
        
        task_obj = Task(
            text=parent_task,
            general_status=due_date,
            priority_index=all_current_tasks+1,
            created_by=request.user
        )

        task_obj.save()

        messages.info(request, "Task has been saved successfully!")

        print(parent_task)
        print(due_date)

    return redirect("/")


def set_priority_index(task_array):
    for task_index in range(len(task_array)):
        priority_index = task_index + 1
        task_id = task_array[task_index]["id"]

        task_object = get_object_or_404(Task, id=task_id)
        task_object.priority_index = priority_index
        task_object.save()

        if task_object.is_parent and 'children' in task_array[task_index]:
            all_chilren = task_array[task_index]["children"]
            set_priority_index(all_chilren)


def update_priority(request):
    output = {'status': True, 'message': 'Login required!'}
    if request.user.is_authenticated:
        if request.method == "GET" and request.is_ajax():
            today = request.GET.get('today')
            tomorrow = request.GET.get('tomorrow')
            week = request.GET.get('week')
            later = request.GET.get('later')

            today = json.loads(today)
            tomorrow = json.loads(tomorrow)
            week = json.loads(week)
            later = json.loads(later)

    

            try:
                set_priority_index(today)
                set_priority_index(tomorrow)
                set_priority_index(week)
                set_priority_index(later)
                
            except Exception as e:
                output['message'] = str(e)
                output['status'] = False


            # print(task_index)
            print(output)
            # print(today)
            # print(tomorrow)
            # print(week)
            # print(later)


            # try:
            #     parent_task = get_object_or_404(Task, id=my_parent_task)
        
            #     new_child_task = Task(
            #         text = child_task_text,
            #         is_parent = False,
            #         status = parent_task.status,
            #         general_status = parent_task.general_status,
            #         created_by = request.user,
            #     )

            #     new_child_task.save()
            #     parent_task.child_task.add(new_child_task)

            #     output['data'] = new_child_task.get_json()
            #     output['message'] = "Success"
            #     output['status'] = True

            # except Exception as e:
            #     output['message'] = str(e)


    return JsonResponse(output)   


def bubbleSort(arr):
    n = len(arr)
 
    # Traverse through all array elements
    for i in range(n):
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j]['priority_index'] > arr[j+1]['priority_index'] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
 


def create_child_task(request):
    output = {'status': False, 'message': 'Login required!'}
    if request.user.is_authenticated:
        if request.method == "GET" and request.is_ajax():
            my_parent_task = request.GET.get('my_parent_task')
            child_task_text = request.GET.get('child_task_text')
           

            try:
                parent_task = get_object_or_404(Task, id=my_parent_task)

                if parent_task.created_by == request.user:

                    all_current_tasks = parent_task.child_task.all().count()
            
                    new_child_task = Task(
                        text = child_task_text,
                        is_parent = False,
                        status = parent_task.status,
                        priority_index = all_current_tasks + 1,
                        general_status = parent_task.general_status,
                        created_by = request.user,
                    )

                    new_child_task.save()
                    parent_task.child_task.add(new_child_task)

                    output['data'] = new_child_task.get_json()
                    output['message'] = "Success"
                    output['status'] = True

                else:
                    output['message'] = "This task doesn't belong to you!"
                    output['status'] = False


            except Exception as e:
                output['message'] = str(e)


    return JsonResponse(output)


def toggle_task(request):
    output = {'status': False, 'message': ''}
    if request.user.is_authenticated:
        if request.method == "GET" and request.is_ajax():
            task_id = request.GET.get("task_id")

            try:
                task = get_object_or_404(Task, id=task_id)
                task.status = 1
                if task.is_parent:
                    task.child_task.all().update(status = 1)
                task.save()
                output['status'] = True
            except Exception as e:
                output['message'] = str(e)


    return JsonResponse(output)


def convert_to_list(queryset):
    return list(queryset)

def create_json_list(array):
    temp_list = []
    for i in array:
        temp_list.append(i.get_json())
    bubbleSort(temp_list)
    return temp_list


@login_required(login_url="/login/")
def index(request):
    all_tasks = Task.objects.filter(is_parent = True, status=0)#.exclude(status = 1)

    today =  all_tasks.filter(general_status='today')
    tomorrow =  all_tasks.filter(general_status='tomorrow')
    week =  all_tasks.filter(general_status='week')
    later =  all_tasks.filter(general_status='later')

    today = convert_to_list(today)
    tomorrow = convert_to_list(tomorrow)
    week = convert_to_list(week)
    later = convert_to_list(later)

    if (today or tomorrow or week or later):
        task_exists = True
    else:
        task_exists = False

    # Completion
    all_tasks_created = Task.objects.filter(created_by = request.user).count()
    count_of_all_task = all_tasks.count()
    all_tasks_done = all_tasks_created - count_of_all_task

    if all_tasks_created > 0:
        percent = (all_tasks_done / all_tasks_created) * 100
        completion_rate = f'{round(percent, 2)}%'
    else:
        completion_rate = None


    TODAY = create_json_list(today)
    TOMORROW = create_json_list(tomorrow)
    WEEK = create_json_list(week)
    LATER = create_json_list(later)


    new_version = []
    if task_exists:
        new_version = [
            ['TODAY', TODAY],
            ['TOMORROW', TOMORROW],
            ['THIS WEEK', WEEK],
            ['LATER', LATER]
        ]
        # new_version = updated_list.copy()
        # for group_index in range(0, len(new_version)):

        #     new_version[group_index] = list(new_version[group_index])
        #     new_version[group_index][1] = list(new_version[group_index][1])

        #     for task_index in range(0, len(new_version[group_index][1])):
        #         task = new_version[group_index][1][task_index]

        #         new_version[group_index][1][task_index] = task.get_json()

        print("===============")
        print(new_version)
        print("===============")

    new_version = json.dumps(new_version)

    all_task_done_objects = Task.objects.filter(created_by = request.user, status = 1)[0:20]

    context = {
        'task_exists': task_exists,
        'completion_rate': completion_rate,
        'completed_tasks': all_task_done_objects,
        'new_version': new_version
    }

    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        segment, active_menu = get_segment(request)

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


def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        active_menu = None

        if segment == '' or segment == 'index.html':
            segment = 'index'
            active_menu = 'dashboard'

        if segment.startswith('dashboard-'):
            active_menu = 'dashboard'

        return segment, active_menu

    except:
        return 'index', 'dashboard'
