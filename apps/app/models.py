from django.db import models
from django.contrib.auth.models import User


# MODEL FOR TASK 
class Task(models.Model):
    text = models.CharField(max_length=255)
    due_date = models.DateField()
    is_parent = models.BooleanField()
    status = models.IntegerField(default=0)
    priority_index = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    child_task = models.ManyToManyField('self', null=True, blank=True)

    def __str__(self):
        return f"{self.text} {'parent' if self.is_parent else 'child'}"

    def statusTranslation(self):
        if self.status == 0:
            return 'Todo'.upper()
        elif self.status == 1:
            return 'Done'.upper()
        elif self.status == -1:
            return 'Overdue'.upper()
        else:
            return None

    def get_child_tasks(self):
        return self.child_task.all()


# MODEL FOR CHILD 
# class Child(models.Model):
#     child_task = models.ForeignKey(Task, on_delete=models.CASCADE) 

