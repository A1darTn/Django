from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Book


def index(request):
    return redirect("books")


def books_view(request):
    template = "books/books_list.html"
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def book_detail(request, pub_date):
    template = ""
    books = Book.objects.filter(pub_date=pub_date)
    page_date = pub_date
    paginator = Paginator(books, 10)
    page = paginator.get_page(page_date)
    context = {"books": books, "page": page}

    return render(request, template, context)
