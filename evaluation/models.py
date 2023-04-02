from django.db import models

class Mentor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'Mentor {self.name}'

class Student(models.Model):
    name = models.CharField(max_length=255)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True,blank=True)
    ideation_marks = models.IntegerField(default=0)
    execution_marks = models.IntegerField(default=0)
    viva_marks = models.IntegerField(default=0)
    marks_locked = models.BooleanField(default=False)

    @property
    def total_marks(self):
        return self.ideation_marks + self.execution_marks + self.viva_marks

    def __str__(self) -> str:
        return f'Student {self.name}'