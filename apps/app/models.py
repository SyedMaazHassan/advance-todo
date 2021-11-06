from django.db import models
from django.contrib.auth.models import User
from django.utils import tree
from django.utils import timezone

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


# MODEL FOR TASK
class Task(models.Model):
    text = models.CharField(max_length=255)
    # due_date = models.DateField(timezone.now)
    is_parent = models.BooleanField(default=True)
    status = models.IntegerField(default=0)
    priority_index = models.IntegerField(default=1)
    general_status = models.CharField(max_length = 10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    child_task = models.ManyToManyField('self', null=True, blank=True)


    def __str__(self):
        return f"{self.text} {'parent' if self.is_parent else 'child'}"


    def bubbleSort(self, arr):
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
    

    def get_json(self):
        list_of_chilren_json = []

        if self.is_parent:
            all_chilren = self.get_childs()
            for i in all_chilren:
                list_of_chilren_json.append(i.get_json())

    
            self.bubbleSort(list_of_chilren_json)

        return {
            'id': self.id,
            'name': self.text,
            'is_parent': self.is_parent,
            'priority_index': self.priority_index,
            'short_text': self.get_short_text(),
            'general_status': self.get_general_status(),
            'status': self.statusTranslation(),
            'children': list_of_chilren_json
        }

    def get_data(self, parent_id):
        return {
            'id': self.id,
            'text': self.text,
            'parent_id': parent_id,
            'status': self.statusTranslation(),
        }

    def get_general_status(self):
        if self.general_status == "week":
            return "this week".upper()
        else:
            return self.general_status.upper()

    def get_childs(self):
        return self.child_task.all().order_by("-id")

    def get_short_text(self):
        length = 30
        if len(self.text) > length:
            return self.text[0: length] + "..."
        return self.text

    def statusTranslation(self):
        if self.status == 0:
            return 'Todo'.upper()
        elif self.status == 1:
            return 'Done'.upper()
        elif self.status == -1:
            return 'Overdue'.upper()
        else:
            return None

    def make_overdue(self):
        self.status = -1

    def get_child_tasks(self):
        return self.child_task.all()


# MODEL FOR CHILD
# class Child(models.Model):
#     child_task = models.ForeignKey(Task, on_delete=models.CASCADE)
