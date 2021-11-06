
    # all_task_object = {
    #     'TODAY': ,
    #     'TOMORROW': all_tasks.filter(general_status='tomorrow'),
    #     'THIS WEEK': all_tasks.filter(general_status='week'),
    #     'LATER': all_tasks.filter(general_status='later')
    # }

    # print("====================")
    # print(str(timezone.localdate()))

    # today_date_format = timezone.localdate()
    # today_string_format = str(timezone.localdate())
    # weekday = timezone.now().weekday()
    # weekday_range = 6 - weekday


    # for single_task in all_tasks:
    #     date_format = single_task.due_date
    #     string_format = str(single_task.due_date)

    #     diff = date_format - today_date_format
    #     diff = diff.days

    #     # Check if task is due overdue.
    #     if diff < 0:
    #         if single_task.status == 0:
    #             single_task.make_overdue()
    #             single_task.save()
    #         all_task_object['OVERDUE'].append(single_task)
    #         continue

    #     # Check if task is due today.
    #     if diff == 0 and string_format == today_string_format:
    #         all_task_object['TODAY'].append(single_task)
    #         continue

    #     # Check if task is due tomorrow.
    #     if diff == 1:
    #         all_task_object['TOMORROW'].append(single_task)
    #         continue

    #     # THis week 
    #     if diff <= weekday_range:
    #         all_task_object['THIS WEEK'].append(single_task)
    #         continue

    #     all_task_object['LATER'].append(single_task)