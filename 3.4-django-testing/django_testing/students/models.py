from django.db import models


class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )
