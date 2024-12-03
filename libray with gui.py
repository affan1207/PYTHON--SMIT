import tkinter as tk
from tkinter import messagebox, ttk
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
                        book.issue_date = datetime.datetime.strptime(issue_date, "%Y-%m-%d") if issue_date != "None" else None
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
            return "Invalid input. Please enter a valid title, author, and year."
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()
        return "Book added successfully!"

    def issue_book(self, title, student):
        issued_count = sum(1 for book in self.books if book.issued_to == student)
        if issued_count >= 3:
            return "Student has reached the maximum limit of 3 books."

        for book in self.books:
            if book.title.lower() == title.lower() and book.status == "Available":
                book.status = "Issued"
                book.issued_to = student
                book.issue_date = datetime.datetime.now()
                self.save_books()
                return f"Book '{title}' issued to {student}."
        return "Book is not available or does not exist."

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.status == "Issued":
                due_date = book.issue_date + datetime.timedelta(days=14)
                if datetime.datetime.now() > due_date:
                    fine = (datetime.datetime.now() - due_date).days * 1
                    messagebox.showinfo("Late Return", f"Book returned late. Fine amount: ${fine}")
                else:
                    messagebox.showinfo("Return", "Book returned on time. No fine.")

                book.status = "Available"
                book.issued_to = None
                book.issue_date = None
                self.save_books()
                return
        messagebox.showerror("Error", "Book is not issued.")

    def delete_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                self.save_books()
                return f"Book '{title}' deleted successfully."
        return "Book not found."

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def show_books(self):
        return self.books


class LibraryApp:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x500")

        # Setting background color
        self.root.configure(bg="#f0f0f0")

        self.login_page()

    def set_button_style(self, button):
        button.configure(bg="#007bff", fg="white", activebackground="#0056b3", activeforeground="white", relief=tk.FLAT)
        button.bind("<Enter>", lambda e: button.configure(bg="#0056b3"))
        button.bind("<Leave>", lambda e: button.configure(bg="#007bff"))

    def login_page(self):
        self.clear_window()

        tk.Label(self.root, text="Admin Login", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

        tk.Label(self.root, text="Username:", bg="#f0f0f0").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:", bg="#f0f0f0").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self.root, text="Login", command=self.login)
        self.set_button_style(login_button)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if any(admin[0] == username and admin[1] == password for admin in self.library.admins):
            self.dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def dashboard(self, username):
        self.clear_window()

        tk.Label(self.root, text=f"Welcome, {username}", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)

        add_book_button = tk.Button(self.root, text="Add Books", width=20, command=self.add_book_page)
        issue_book_button = tk.Button(self.root, text="Issue Books", width=20, command=self.issue_book_page)
        return_book_button = tk.Button(self.root, text="Return Books", width=20, command=self.return_book_page)
        show_books_button = tk.Button(self.root, text="Show All Books", width=20, command=self.show_books_page)
        logout_button = tk.Button(self.root, text="Logout", width=20, command=self.login_page)

        # Applying the button style
        for button in [add_book_button, issue_book_button, return_book_button, show_books_button, logout_button]:
            self.set_button_style(button)
            button.pack(pady=10)

    def add_book_page(self):
        self.clear_window()

        tk.Label(self.root, text="Add New Book", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)

        tk.Label(self.root, text="Title:", bg="#f0f0f0").pack()
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        tk.Label(self.root, text="Author:", bg="#f0f0f0").pack()
        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack()

        tk.Label(self.root, text="Year:", bg="#f0f0f0").pack()
        self.year_entry = tk.Entry(self.root)
        self.year_entry.pack()

        add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.set_button_style(add_book_button)
        add_book_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Back to Dashboard", command=lambda: self.dashboard("Admin"))
        self.set_button_style(back_button)
        back_button.pack(pady=10)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        message = self.library.add_book(title, author, year)
        messagebox.showinfo("Add Book", message)

    def issue_book_page(self):
        self.clear_window()

        tk.Label(self.root, text="Issue Book", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)

        tk.Label(self.root, text="Book Title:", bg="#f0f0f0").pack()
        self.issue_title_entry = tk.Entry(self.root)
        self.issue_title_entry.pack()

        tk.Label(self.root, text="Student Name:", bg="#f0f0f0").pack()
        self.student_name_entry = tk.Entry(self.root)
        self.student_name_entry.pack()

        issue_book_button = tk.Button(self.root, text="Issue Book", command=self.issue_book)
        self.set_button_style(issue_book_button)
        issue_book_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Back to Dashboard", command=lambda: self.dashboard("Admin"))
        self.set_button_style(back_button)
        back_button.pack(pady=10)

    def issue_book(self):
        title = self.issue_title_entry.get()
        student = self.student_name_entry.get()
        message = self.library.issue_book(title, student)
        messagebox.showinfo("Issue Book", message)

    def return_book_page(self):
        self.clear_window()

        tk.Label(self.root, text="Return Book", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)

        tk.Label(self.root, text="Book Title:", bg="#f0f0f0").pack()
        self.return_title_entry = tk.Entry(self.root)
        self.return_title_entry.pack()

        return_book_button = tk.Button(self.root, text="Return Book", command=self.return_book)
        self.set_button_style(return_book_button)
        return_book_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Back to Dashboard", command=lambda: self.dashboard("Admin"))
        self.set_button_style(back_button)
        back_button.pack(pady=10)

    def return_book(self):
        title = self.return_title_entry.get()
        self.library.return_book(title)

    def show_books_page(self):
        self.clear_window()

        tk.Label(self.root, text="Library Books", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)

        columns = ("Title", "Author", "Year", "Status")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(pady=10)

        books = self.library.show_books()
        for book in books:
            tree.insert("", tk.END, values=(book.title, book.author, book.year, book.status))

        back_button = tk.Button(self.root, text="Back to Dashboard", command=lambda: self.dashboard("Admin"))
        self.set_button_style(back_button)
        back_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
