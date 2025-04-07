from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Book


def index(request):
    return redirect("books")


def books_view(request):
    template = "books/books_list.html"
    books = Book.objects.all()
    context = {"books": books}
    return render(request, template, context)


def book_detail(request, pub_date):
    template = "books/book_detail.html" 
    books = Book.objects.filter(pub_date=pub_date).first() #Объясните, пожалуйста, почему без first() не работало
    page_date = pub_date
    paginator = Paginator(books, 10)
    page = paginator.get_page(page_date)
    books = page.object_list
    context = {
        "books": books,
        "page": page
    }

    return render(request, template, context)
