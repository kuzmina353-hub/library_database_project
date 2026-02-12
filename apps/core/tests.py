from datetime import date
from django.test import TestCase

from .models import Author, Genre, Publishing, Book, Reader, Phone, Lending, Address, Variety, Gender

# Create your tests here.
class AuthorModelTest(TestCase):
    def setUp(self):
        self.author_data = {
            "surname": "King",
            "first_name": "Stephen",
            "last_name": "Edwin",
            "birth_date": "1947-09-21",
            "gender" : Gender.MALE,
        }
        self.author = Author.objects.create(**self.author_data)

    def test_create_author(self):
        author = Author.objects.get(id=self.author.id)
        self.assertEqual(author.surname, self.author_data["surname"])
        self.assertEqual(author.first_name, self.author_data["first_name"])
        self.assertEqual(author.gender, Gender.MALE)

    def test_read_author(self):
        author = Author.objects.get(id=self.author.id)
        self.assertEqual(author.first_name, "Stephen")

    def test_update_author(self):
        self.author.first_name = "Steve"
        self.author.save()
        updated_author = Author.objects.get(id=self.author.id)
        self.assertEqual(updated_author.first_name, "Steve")

    def test_delete_author(self):
        author_id = self.author.id
        self.author.delete()
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(id=author_id)

class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Horror")

    def test_create_genre(self):
        genre = Genre.objects.get(id=self.genre.id)
        self.assertEqual(genre.name, "Horror")

    def test_update_genre(self):
        self.genre.name = "Thriller"
        self.genre.save()
        self.assertEqual(
            Genre.objects.get(id=self.genre.id).name,
            "Thriller"
        )

    def test_delete_genre(self):
        genre_id = self.genre.id
        self.genre.delete()
        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(id=genre_id)

class PublishingModelTest(TestCase):
    def setUp(self):
        self.publishing = Publishing.objects.create(
            name="Viking Press",
            country="USA",
            city="New York"
        )

    def test_create_publishing(self):
        self.assertEqual(self.publishing.name, "Viking Press")

    def test_update_publishing(self):
        self.publishing.city = "Brooklyn"
        self.publishing.save()
        self.assertEqual(
            Publishing.objects.get(id=self.publishing.id).city,
            "Brooklyn"
        )

    def test_delete_publishing(self):
        pub_id = self.publishing.id
        self.publishing.delete()
        with self.assertRaises(Publishing.DoesNotExist):
            Publishing.objects.get(id=pub_id)

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            surname="King",
            first_name="Stephen",
            last_name="Edwin"
        )
        self.genre = Genre.objects.create(name="Horror")
        self.publishing = Publishing.objects.create(
            name="Viking Press",
            country="USA",
            city="New York"
        )
        self.book = Book.objects.create(
            title="It",
            genre=self.genre,
            publishing=self.publishing,
            isbn="06-708-13-028",
            year_published=1986,
            available_copies=2,
            variety=Variety.PAPERBACK
        )
        self.book.author.add(self.author)

    def test_create_book(self):
        self.assertEqual(self.book.title, "It")

    def test_read_book(self):
        book = Book.objects.get(id=self.book.id)
        self.assertEqual(book.author.first().surname, "King")

    def test_update_book(self):
        self.book.title = "'It' updated."
        self.book.save()
        self.assertEqual(
            Book.objects.get(id=self.book.id).title,
            "'It' updated."
        )

    def test_delete_book(self):
        book_id = self.book.id
        self.book.delete()
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book_id)


class ReaderModelTest(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create(
            surname="Johnson",
            first_name="John",
            last_name="Michael",
            email="john@email.com",
            gender=Gender.MALE
        )

    def test_create_reader(self):
        self.assertEqual(self.reader.first_name, "John")

    def test_update_reader(self):
        self.reader.first_name = "James"
        self.reader.save()
        self.assertEqual(
            Reader.objects.get(id=self.reader.id).first_name,
            "James"
        )

    def test_delete_reader(self):
        reader_id = self.reader.id
        self.reader.delete()
        with self.assertRaises(Reader.DoesNotExist):
            Reader.objects.get(id=reader_id)


class LendingModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            surname="King",
            first_name="Stephen",
            last_name="Edwin"
        )
        self.genre = Genre.objects.create(name="Horror")
        self.publishing = Publishing.objects.create(
            name="Viking Press",
            country="USA",
            city="New York"
        )
        self.book = Book.objects.create(
            title="It",
            genre=self.genre,
            publishing=self.publishing,
            isbn="06-708-13-029",
            year_published=1986,
            available_copies=2,
            variety=Variety.PAPERBACK
        )
        self.book.author.add(self.author)
        self.reader = Reader.objects.create(
            surname="Johnson",
            first_name="John",
            last_name="Michael",
            email="john@email.com",
            gender=Gender.MALE )

    def test_lending_less_copies(self):
        lending = Lending.objects.create(
            book=self.book,
            reader=self.reader,
            lending_date=date.today()
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)

    def test_return_increase_copies(self):
        lending = Lending.objects.create(
            book=self.book,
            reader=self.reader,
            lending_date=date.today()
        )
        lending.returned = True
        lending.save()
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)

class PhoneModelTest(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create(
            surname="Johnson",
            first_name="John",
            last_name="Michael",
            email="john@email.com",
            gender=Gender.MALE
        )
        self.phone = Phone.objects.create(
            reader=self.reader,
            phone="+380000000"
        )

    def test_create_phone(self):
        self.assertEqual(self.phone.reader.first_name, "John")

    def test_update_phone(self):
        self.phone.phone = "+380000001"
        self.phone.save()
        self.assertEqual(
            Phone.objects.get(id=self.phone.id).phone,
            "+380000001"
        )

    def test_delete_phone(self):
        phone_id = self.phone.id
        self.phone.delete()
        with self.assertRaises(Phone.DoesNotExist):
            Phone.objects.get(id=phone_id)


class AddressModelTest(TestCase):

    def setUp(self):
        self.reader = Reader.objects.create(
            surname="Johnson",
            first_name="John",
            last_name="Michael",
            email="john@email.com",
            gender=Gender.MALE
        )
        self.address = Address.objects.create(
            reader=self.reader,
            country="USA",
            region="NY",
            area="Manhattan",
            city="New York",
            street="Main Avenue",
            building="10",
            apartment="1A"
        )

    def test_create_address(self):
        self.assertEqual(self.address.city, "New York")

    def test_update_address(self):
        self.address.street = "Main Street"
        self.address.save()
        self.assertEqual(
            Address.objects.get(id=self.address.id).street,
            "Main Street"
        )

    def test_delete_address(self):
        address_id = self.address.id
        self.address.delete()
        with self.assertRaises(Address.DoesNotExist):
            Address.objects.get(id=address_id)
