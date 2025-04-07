from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Book


def index(request):
    return redirect("books")


def books_view(request):
    template = "books/books_list.html"
    books = Book.objects.all()
    context = {"books": books}
    return render(request, template, context)


# def book_detail(request, pub_date):
#     template = "books/book_detail.html" 
#     books = Book.objects.filter(pub_date=pub_date).first()
#     page_date = pub_date
#     paginator = Paginator(books, 10)
#     page = paginator.get_page(page_date)
#     print(page)
#     context = {
#         "books": books,
#         "page": page
#     }

#     return render(request, template, context) 

def book_detail(request, pub_date):
    target_date = timezone.datetime.strptime(pub_date, '%Y-%m-%d').date()

    # Получаем все книги, отсортированные по дате
    all_books = Book.objects.all().order_by('pub_date')

    # Ищем индекс книги с выбранной датой
    book_index = next((index for index, book in enumerate(all_books) if book.pub_date == target_date), None)

    if book_index is not None:
        previous_book = all_books[book_index - 1] if book_index > 0 else None
        next_book = all_books[book_index + 1] if book_index < len(all_books) - 1 else None
        current_book = all_books[book_index]
    else:
        previous_book = None
        next_book = None
        current_book = None

    # Отображение книги по выбранной дате
    return render(request, 'books/book_detail.html', {
        'current_book': current_book,
        'previous_book': previous_book,
        'next_book': next_book,
    })
