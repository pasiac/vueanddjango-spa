from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name}'


class Task(models.Model):
    TODO = 'todo'
    DONE = 'done'

    STATUS_CHOICES = (
        (TODO, 'Todo'),
        (DONE, 'Done')
    )

    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=TODO)
    started = models.DateField(auto_now_add=True)
    minutes_spend = models.IntegerField(default=0)
    enjoyed = models.BooleanField(default=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
