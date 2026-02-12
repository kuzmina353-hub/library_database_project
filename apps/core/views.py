from django.shortcuts import render
from apps.core.models import Book, Variety, Gender, Reader, Author, Genre, Publishing, Lending


# Create your views here.
def home(request):
    return render(request, 'core/home.html',
                  {'title': 'Welcome to the Library'})

def about_project(request):
    description = {
        'name_of_project': 'Library Database',
        'description': """This is the Library database project.

        You can create Authors, Books and Readers lists here.

        To borrow a book from the Library use the Lend Page.

        Good Luck! :-)
        """
    }
    return render(request, 'about.html', description)

def books(request):
    if request.method == 'POST':
        genre_id = request.POST.get('genre_select')
        genre_name = request.POST.get('genre_new', '').strip()
        if genre_id:
            genre = Genre.objects.get(id=genre_id)
        elif genre_name:
            genre, _ = Genre.objects.get_or_create(name=genre_name)
        else:
            genre = None
        pub_id = request.POST.get('publishing_select')
        pub_name = request.POST.get('publishing_new', '').strip()
        if pub_id:
            publishing = Publishing.objects.get(id=pub_id)
        elif pub_name:
            publishing, _ = Publishing.objects.get_or_create(name=pub_name)
        else:
            publishing = None
        book = Book.objects.create(
            title=request.POST.get('title', ''),
            genre=genre,
            publishing=publishing,
            available_copies=int(request.POST.get('available_copies', 1)),
            variety=request.POST.get('variety', None),
            isbn=request.POST.get('isbn', '').strip() or None,
            year_published=request.POST.get('year_published') or None,
        )
        author_name = request.POST.get('author', '').strip()
        if author_name:
            parts = author_name.split()
            first_name = parts[0]
            surname = " ".join(parts[1:]) if len(parts) > 1 else ""
            author, _ = Author.objects.get_or_create(first_name=first_name, surname=surname)
            book.author.add(author)
    return render(
        request,
        'core/books.html',
        {
            "variety_choices": Variety.choices,
            "book_list": Book.objects.all(),
            "authors": Author.objects.all(),
            "genres": Genre.objects.all(),
            "publishings": Publishing.objects.all(),
        }
    )


def readers(request):
    if request.method == 'POST':
        reader = Reader.objects.create(
            surname=request.POST.get('surname', ''),
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            birth_date=request.POST.get('birth_date') or None,
            email=request.POST.get('email', '').strip(),
            gender=request.POST.get('gender', None),
        )
        print(reader)
    return render(request, 'core/readers.html',
                  {"gender_choices": Gender.choices, "readers": Reader.objects.all()})

def authors(request):
    if request.method == 'POST':
        author = Author.objects.create(
            surname=request.POST.get('surname', ''),
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            birth_date=request.POST.get('birth_date') or None,
            gender=request.POST.get('gender', None),
        )
        print(author)
    return render(request, 'core/authors.html',
                  {"gender_choices": Gender.choices, "authors": Author.objects.all()})

def genres(request):
    if request.method == 'POST':
        genre = Genre.objects.create(
            name=request.POST.get('name', ''),
        )
        print(genre)
    return render(request, 'core/genre.html',
                  {"genres": Genre.objects.all()})

def publishing(request):
    if request.method == 'POST':
        publisher = Publishing.objects.create(
            name=request.POST.get('name', ''),
            country=request.POST.get('country', ''),
            city=request.POST.get('city', ''),
        )
        print(publisher)
    return render(request, 'core/publishing.html',
                  {"publishings": Publishing.objects.all()})


def lend_page(request):
    message = ""
    if request.method == "POST":
        return_lending_id = request.POST.get("return_lending_id")
        if return_lending_id:
            try:
                lending = Lending.objects.get(id=return_lending_id)
                if not lending.returned:
                    lending.returned = True
                    lending.save()
                    message = "Book returned."
                else:
                    message = "This book is already returned."
            except Lending.DoesNotExist:
                message = "Lending not found."
        else:
            reader_id = request.POST.get("reader")
            book_id = request.POST.get("book")
            if not reader_id or not book_id:
                message = "Please select both reader and book."
            else:
                try:
                    reader = Reader.objects.get(id=reader_id)
                    book = Book.objects.get(id=book_id)
                    if book.available_copies > 0:
                        Lending.objects.create(reader=reader, book=book)
                        message = "Book successfully lent."
                    else:
                        message = "No available copies."

                except Reader.DoesNotExist:
                    message = "Selected reader not found."
                except Book.DoesNotExist:
                    message = "Selected book not found."
    readers = Reader.objects.all()
    books = Book.objects.filter(available_copies__gt=0)
    lendings = Lending.objects.filter(returned=False)
    return render(request, "core/lend.html", {
        "readers": readers,
        "books": books,
        "lendings": lendings,
        "message": message
    })



