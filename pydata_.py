import re
import mysql.connector
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog
import tkinter.messagebox
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------------------------------------------
connection = mysql.connector.connect(
    host='localhost',
    user='Yuvraj',
    password='yuvraj1234',
    database='Register'
)


# -----------------------------------------------------------------------------------------------------------------
def main():
    # -----------------------------------------------------------------------------------------------------------------
    def add_book():
        def subbmit():
            add_books_name = entry_books.get().split(",")
            books = [book.strip() for book in add_books_name]
            cleaned_book_name = set(books)
            books_to_insert = []

            for book in cleaned_book_name:
                quantity = tkinter.simpledialog.askstring("Quantity", f"How many of '{book}' to stock?")
                while not quantity or not quantity.isdigit():
                    tkinter.messagebox.showerror("Invalid input", "Enter a valid positive number")
                    quantity = tkinter.simpledialog.askstring("Quantity", f"How many of '{book}' to stock?")
                quantity = int(quantity)

                author = tkinter.simpledialog.askstring("Author", f"Who is the author of '{book}'?")
                genre = tkinter.simpledialog.askstring("Genre", f"What is the genre of '{book}'?")
                year = tkinter.simpledialog.askstring("Publication Year", f"When was '{book}' published?")
                while not (year and year.isdigit() and len(year) == 4):
                    tkinter.messagebox.showerror("Invalid input", "Enter a valid 4-digit year")
                    year = tkinter.simpledialog.askstring("Publication Year", f"When was '{book}' published?")

                books_to_insert.append((book.strip().title(), author.strip().title(), genre.strip().title(), int(year), quantity))

            insert = '''INSERT INTO manage_books (Title, Author, Genre, Publication_Year, Quantity) VALUES (%s, %s, %s, %s, %s)'''
            for data in books_to_insert:
                cursor.execute(insert, data)
            connection.commit()
            tkinter.messagebox.showinfo("Success", "Books added successfully")

        root = tk.Toplevel()
        root.iconbitmap("library_icon.ico")
        root.config(bg="black")
        root.title("Add Books")
        tk.Label(root, bg="grey", fg="white", text="Enter book names (comma-separated):").grid(row=0, column=0, padx=10,pady=20)
        entry_books = tk.Entry(root, width=50)
        entry_books.grid(row=0, column=1, padx=20,pady=20)
        tk.Button(root, text="Submit", command=subbmit).grid(row=3, column=1, pady=20)
        root.mainloop()

    # -----------------------------------------------------------------------------------------------------------------
    def add_member():
        def subbbmit():
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            phone_pattern = r"^[6-9]\d{9}$"

            members = [m.strip() for m in entry_member.get().split(",")]
            cleaned_members = set(members)
            members_to_insert = []

            for member in cleaned_members:
                date_str = tkinter.simpledialog.askstring("Joining Date", f"Date of joining for {member} (YYYY-MM-DD):")
                try:
                    join_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except:
                    tkinter.messagebox.showerror("Invalid date", "Enter a valid date in YYYY-MM-DD format")
                    continue

                email = tkinter.simpledialog.askstring("Email", f"Email of {member}:")
                while not re.match(email_pattern, email):
                    tkinter.messagebox.showerror("Invalid email", "Enter a valid email")
                    email = tkinter.simpledialog.askstring("Email", f"Email of {member}:")

                phone = tkinter.simpledialog.askstring("Phone", f"Phone number of {member}:")
                while not re.match(phone_pattern, phone):
                    tkinter.messagebox.showerror("Invalid phone", "Enter a valid 10-digit number starting with 6-9")
                    phone = tkinter.simpledialog.askstring("Phone", f"Phone number of {member}:")

                members_to_insert.append((member.title(), join_date, email, phone))

            insert = '''INSERT INTO manage_members (Name, Membership_Date, Email, Phone) VALUES (%s, %s, %s, %s)'''
            for data in members_to_insert:
                cursor.execute(insert, data)
            connection.commit()
            tkinter.messagebox.showinfo("Success", "Members added successfully")

        root = tk.Toplevel()
        root.config(bg="black")
        root.iconbitmap("library_icon.ico")
        root.title("Add Member")
        tk.Label(root,bg="grey",fg="white", text="Enter members (comma-separated):").grid(row=0, column=0,padx=10,pady=20)
        entry_member = tk.Entry(root, width=50)
        entry_member.grid(row=0, column=1,padx=20,pady=20)
        tk.Button(root, text="Submit", command=subbbmit).grid(row=1, column=1,padx=20)
        root.mainloop()

    # -----------------------------------------------------------------------------------------------------------------
    def delete_book():
        def subbbbbbmit():
            book = enter_ID_B.get().strip()
            b = int(book)
            cursor.execute("DELETE FROM manage_borrowed_books WHERE BookID = %s", (b,))
            connection.commit()
            cursor.execute("DELETE from manage_books WHERE BookID = %s", (b,))
            connection.commit()
            tkinter.messagebox.showinfo("Books","Books deleted succesfully")

        root = tk.Tk()
        root.iconbitmap("library_icon.ico")
        root.config(bg="black")
        root.title("Delete books")
        tk.Label(root,text="Enter Book ID (Seperated by commas)",fg="white",bg="grey").grid(row=0,column=0,padx=10,pady=20)
        enter_ID_B = tk.Entry(root, width=50)
        enter_ID_B.grid(row=0, column=1,padx=20,pady=20)
        tk.Button(root, text="Delete", command=subbbbbbmit).grid(row=1,column=1,padx=20,pady=20)

    # -----------------------------------------------------------------------------------------------------------------
    def view_books():
        cursor.execute("SELECT * FROM manage_books")
        books = cursor.fetchall()

        root = tk.Toplevel()
        root.title("View Books")
        root.config(bg="black")
        root.iconbitmap("library_icon.ico")

        # Treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black", rowheight=25)
        style.map("Treeview", background=[('selected', '#333')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background="grey20", foreground="white", font=('Arial', 10, 'bold'))

        # Frame to hold tree and scrollbar
        frame = tk.Frame(root, bg="black")
        frame.pack(expand=True, fill=tk.BOTH)

        cols = ("ID", "Title", "Author", "Genre", "Year", "Quantity")
        tree = ttk.Treeview(frame, columns=cols, show="headings", style="Treeview")
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)

        for row in books:
            tree.insert("", tk.END, values=row)

        tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Make the frame expandable
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)



     # -----------------------------------------------------------------------------------------------------------------
    def view_members():
        cursor.execute("SELECT * FROM manage_members")
        members = cursor.fetchall()
        root = tk.Toplevel()
        root.title("View member")
        root.config(bg="black")
        root.iconbitmap("library_icon.ico")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black", rowheight=25)
        style.map("Treeview", background=[('selected', '#333')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background="grey20", foreground="white", font=('Arial', 10, 'bold'))

        # Frame to hold tree and scrollbar
        frame = tk.Frame(root, bg="black")
        frame.pack(expand=True, fill=tk.BOTH)

        cols = ("MemberID", "Name", "Email", "Phone", "Membership_Date")
        tree = ttk.Treeview(frame, columns=cols, show="headings", style="Treeview")
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)

        for row in members:
            tree.insert("", tk.END, values=row)

        tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Make the frame expandable
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
    # -----------------------------------------------------------------------------------------------------------------
    def borrow_book():
        def subbbmit():
            member_id = entry_m_id.get().strip()
            book_id = entry_b_id.get().strip()          
            cursor.execute("SELECT Quantity FROM manage_books WHERE BookID = %s", (book_id,))
            result = cursor.fetchone()

            if result is None:
                tkinter.messagebox.showerror("Error", "Book not found")
                return
            quantity = result[0]
            if quantity <= 0:
                tkinter.messagebox.showinfo("Out of stock", "Book is currently out of stock")
                return

            else:
                borrow_date = datetime.today().date()
                due_date = borrow_date + timedelta(days=14)
                cursor.execute('''INSERT INTO manage_borrowed_books (MemberID, BookID, BorrowDate, DueDate, Fine)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (member_id, book_id, borrow_date, due_date, 0.00))

                cursor.execute("UPDATE manage_books SET Quantity = Quantity - 1 WHERE BookID = %s", (book_id,))
                connection.commit()
                tkinter.messagebox.showinfo("Success", f"Book borrowed. Due on: {due_date}")

        root = tk.Toplevel()
        root.iconbitmap("library_icon.ico")
        root.config(background="black")
        root.title("Borrow Book")
        tk.Label(root,bg="grey",fg="white", text="Member ID").grid(row=0, column=0, padx=10,pady=20)
        entry_m_id = tk.Entry(root, width=50)
        entry_m_id.grid(row=0, column=1,padx=20,pady=20)
        tk.Label(root,bg="grey",fg="white", text="Book ID").grid(row=1, column=0)
        entry_b_id = tk.Entry(root, width=50)
        entry_b_id.grid(row=1, column=1,padx=20,pady=20)
        tk.Button(root, text="Submit", command=subbbmit).grid(row=2, column=1,padx=20,pady=20)
        root.mainloop()

    # -----------------------------------------------------------------------------------------------------------------
    def return_book():
        def subbbbbmit():
            member_id = entry_m_id.get().strip()
            book_id = entry_b_id.get().strip()
            if not member_id or not book_id:
                tkinter.messagebox.showwarning("Emty","All the entries must be filled")
            else:
                cursor.execute('''SELECT BorrowID, DueDate FROM manage_borrowed_books 
                                  WHERE MemberID = %s AND BookID = %s AND ReturnDate IS NULL''',
                               (member_id, book_id))
                record = cursor.fetchone()

                if not record:
                    tkinter.messagebox.showwarning("Not Found", "No active borrow record found")
                    return

                borrow_id, due_date = record
                return_date = datetime.today().date()

                overdue_days = (return_date - due_date).days
                fine = 5 * overdue_days if overdue_days > 0 else 0

                cursor.execute('''UPDATE manage_borrowed_books 
                                  SET ReturnDate = %s, Fine = %s 
                                  WHERE BorrowID = %s''',
                               (return_date, fine, borrow_id))

                cursor.execute("UPDATE manage_books SET Quantity = Quantity + 1 WHERE BookID = %s", (book_id,))
                connection.commit()

                msg = f"Book returned successfully.{'\nLate fee: ₹'+str(fine) if fine > 0 else '\nNo fine.'}"
                tkinter.messagebox.showinfo("Return Info", msg)

        root = tk.Toplevel()
        root.config(background="black")
        root.iconbitmap("library_icon.ico")
        root.title("Return Book")

        tk.Label(root, fg="white", bg="grey", text="Member ID").grid(row=0, column=0, pady=20,padx=10)
        entry_m_id = tk.Entry(root, width=50)
        entry_m_id.grid(row=0, column=1, pady=20,padx=25)
        tk.Label(root, fg="white", bg="grey", text="Book ID").grid(row=1, column=0, pady=20)
        entry_b_id = tk.Entry(root, width=50)
        entry_b_id.grid(row=1, column=1)
        tk.Button(root, text="Submit", command=subbbbbmit).grid(row=2, column=1, pady=20)
        root.mainloop()


    root = tk.Tk()
    root.iconbitmap("library_icon.ico")
    root.config(background="black")
    root.title("Library manager")
    tk.Button(root,bg="grey",fg="white", text="Add Books", command=add_book).grid(row=0, column=1, padx= 20,pady=20)
    tk.Button(root,bg="grey",fg="white", text="Add Members", command=add_member).grid(row=0, column=2, padx= 20,pady=20)
    tk.Button(root,bg="grey",fg="white", text="View Books", command=view_books).grid(row=1, column=1, padx= 20,pady=20)
    tk.Button(root,bg="grey",fg="white",  text="View Members", command=view_members).grid(row=1, column=2, padx= 20,pady=20)
    tk.Button(root,bg="grey",fg="white", text="Borrow Books", command=borrow_book).grid(row=2, column=1, padx= 20,pady=20)
    tk.Button(root,bg="grey",fg="white", text="Return Book", command=return_book).grid(row=2, column=2, padx= 20,pady=20)
    tk.Button(root,bg="grey",fg="white", text="Delete Book", command=delete_book).grid(row=3, column=1, padx= 20,pady=20)
    tk.Button(root,bg="grey",fg="white", text="Exit", command=exit).grid(row=3, column=2, padx= 20,pady=20)
    root.mainloop()


    # -----------------------------------------------------------------------------------------------------------------
if connection.is_connected():
    print("connected to server")
    cursor = connection.cursor()
    main()
