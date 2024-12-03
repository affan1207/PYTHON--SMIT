import datetime

class Book:
    def __init__(self, title, author, year, status="Available"):
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.issued_to = None
        self.issue_date = None


class Library:
    def __init__(self):
        self.books = self.load_books()
        self.admins = self.load_admins()

    def load_books(self):
        try:
            with open("books.txt", "r") as file:
                books = []
                for line in file:
                    try:
                        title, author, year, status, issued_to, issue_date = line.strip().split(",")
                        book = Book(title, author, year, status)
                        book.issued_to = issued_to if issued_to != "None" else None
                        book.issue_date = datetime.datetime.strptime(issue_date,
                                                                     "%Y-%m-%d") if issue_date != "None" else None
                        books.append(book)
                    except ValueError:
                        print(f"Error parsing line: {line}")
                return books
        except FileNotFoundError:
            return []

    def save_books(self):
        with open("books.txt", "w") as file:
            for book in self.books:
                issued_to = book.issued_to if book.issued_to else "None"
                issue_date = book.issue_date.strftime("%Y-%m-%d") if book.issue_date else "None"
                file.write(f"{book.title},{book.author},{book.year},{book.status},{issued_to},{issue_date}\n")

    def load_admins(self):
        try:
            with open("admins.txt", "r") as file:
                admins = []
                for line in file:
                    username, password = line.strip().split(",")
                    admins.append((username, password))
                return admins
        except FileNotFoundError:
            return []

    def save_admins(self):
        with open("admins.txt", "w") as file:
            for admin in self.admins:
                file.write(f"{admin[0]},{admin[1]}\n")

    def add_book(self, title, author, year):
        if not title or not author or not year.isdigit():
            print("Invalid input. Please enter valid title, author, and year.")
            return
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()

    def issue_book(self, title, student):
        issued_count = sum(1 for book in self.books if book.issued_to == student)
        if issued_count >= 3:
            print("Student has reached the maximum limit of 3 books.")
            return

        for book in self.books:
            if book.title.lower() == title.lower() and book.status == "Available":
                book.status = "Issued"
                book.issued_to = student
                book.issue_date = datetime.datetime.now()
                self.save_books()
                print(f"Book '{title}' issued to {student}.")
                return
        print("Book is not available or does not exist.")

    def edit_book(self, title, author=None, year=None):
        for book in self.books:
            if book.title.lower() == title.lower():
                if author:
                    book.author = author
                if year and year.isdigit():
                    book.year = year
                self.save_books()
                print(f"Book '{title}' updated successfully.")
                return
        print("Book not found.")

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.status == "Issued":
                due_date = book.issue_date + datetime.timedelta(days=14)  # Assume 2 weeks is the borrow period
                if datetime.datetime.now() > due_date:
                    fine = (datetime.datetime.now() - due_date).days * 1  # Assume fine is $1 per day
                    print(f"Book returned late. Fine amount: ${fine}")
                else:
                    print("Book returned on time. No fine.")

                book.status = "Available"
                book.issued_to = None
                book.issue_date = None
                self.save_books()
                return
        print("Book is not issued.")

    def delete_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                self.save_books()
                print(f"Book '{title}' deleted successfully.")
                return
        print("Book not found.")

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def show_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        for book in self.books:
            print(f"Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")


def login(admins, username, password):
    for admin in admins:
        if admin[0] == username and admin[1] == password:
            return True
    return False


def change_password(admins, username, old_password, new_password):
    for i, admin in enumerate(admins):
        if admin[0] == username and admin[1] == old_password:
            admins[i] = (username, new_password)
            return True
    return False


def dashboard(library, username):
    while True:
        print(f"\nWelcome, {username}!")
        print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
        print("1. Add Books")
        print("2. Issue Books")
        print("3. Edit Books")
        print("4. Return Books")
        print("5. Delete Books")
        print("6. Search Books")
        print("7. Show Books")
        print("8. Log out")
        choice = input("Choose an option: ")
        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            year = input("Enter book year: ").strip()
            library.add_book(title, author, year)
        elif choice == "2":
            title = input("Enter book title: ").strip()
            student = input("Enter student name: ").strip()
            library.issue_book(title, student)
        elif choice == "3":
            title = input("Enter book title: ").strip()
            author = input("Enter new author (leave blank if unchanged): ").strip()
            year = input("Enter new year (leave blank if unchanged): ").strip()
            library.edit_book(title, author, year)
        elif choice == "4":
            title = input("Enter book title: ").strip()
            library.return_book(title)
        elif choice == "5":
            title = input("Enter book title: ").strip()
            library.delete_book(title)
        elif choice == "6":
            title = input("Enter book title: ").strip()
            book = library.search_book(title)
            if book:
                print(f"Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")
                print(f"Issued to: {book.issued_to}, Issue Date: {book.issue_date}")
            else:
                print("Book not found.")
        elif choice == "7":
            library.show_books()
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")


def main():
    library = Library()
    while True:
        print("Admin Panel")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        if login(library.admins, username, password):
            print("Login successful!")
            dashboard(library, username)
            if input("Do you want to log in again? (y/n): ").lower() != 'y':
                break
        else:
            print("Invalid credentials. Please try again.")


if __name__ == "__main__":
    main()
