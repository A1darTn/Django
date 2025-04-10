from django.shortcuts import render
from django.http import HttpResponse
from .models import Student


def students_list(request):
    template = "school/students_list.html"
    ordering = "group"
    object_list = Student.objects.prefetch_related('teacher').order_by(ordering)
    context = {"object_list": object_list}

    return render(request, template, context)


def sample_view(request):
    html = "<body><h1>Django sample_view</h1><br><p>Отладка sample_view</p></body>"
    return HttpResponse(html)
