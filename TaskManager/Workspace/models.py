from django.db import models

# Create your models here.
class Tasks(models.Model):
    task_name = models.TextField(max_length=50)
    description = models.TextField(max_length=200, default="Add Description")
    due_date = models.DateField()
    completion = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task_name}'