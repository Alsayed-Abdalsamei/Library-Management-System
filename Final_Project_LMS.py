import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from PIL import Image, ImageTk # type: ignore
import sqlite3
content = None


def create_database():
   
    try:
        # إنشاء أو الاتصال بقاعدة البيانات
        db = sqlite3.connect("books.db")
        cr = db.cursor()

        # إنشاء جدول الكتب إذا لم يكن موجودًا
        cr.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                book_title TEXT,
                author TEXT,
                genre TEXT,
                copies INTEGER
            )
        """)

        
        # حفظ التغييرات
        db.commit()

        db.close()

       
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")



    #_______________________
    
    connection = sqlite3.connect('students.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER ,
                        name TEXT,
                        branch TEXT,
                        contact TEXT)''')
    connection.commit()
    connection.close()
    #_____________________
    tr = sqlite3.connect('transactions.db')
    cursor = tr.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        book_id INTEGER,
        date_borrowed TEXT,
        date_returned TEXT
    )
    ''')
    

    tr.commit()
    tr.close()

create_database()
    

# Function to open the library management system
def open_library_system():
    # وظيفة لحفظ بيانات الطالب في قاعدة البيانات
    def save_student():
        student_id = entry_student_id.get().strip()
        student_name = entry_student_name.get().strip()
        branch_name = entry_branch_name.get().strip()
        contact_number = entry_contact_number.get().strip()

        # التحقق من أن جميع الحقول مكتملة
        if not student_id or not student_name or not branch_name or not contact_number:
            messagebox.showerror("Input Error", "All fields are required!")
            return
        if not student_id.isdigit():
            messagebox.showerror("Input Error", "student id must be numeric values.")
            return
        if not isinstance(student_name, str) or not student_name.replace(" ", "").isalpha():
            messagebox.showerror("Input Error", "Student name must be a valid string containing only letters.")
            return
      
        # التحقق من أن branch_name هو نص (string)
        if not isinstance(branch_name, str) or not branch_name.replace(" ", "").isalpha():
            messagebox.showerror("Input Error", "Student section must be a valid string containing only letters.")
            return
        
        # التحقق من صحة رقم الهاتف (يجب أن يكون 11 رقمًا)
        if not contact_number.isdigit() or len(contact_number) != 11:
            messagebox.showerror("Input Error", "Invalid contact number. It must be an 11-digit number.")
            return
        
        # إضافة بيانات الطالب إلى قاعدة البيانات
        try:
            # فتح الاتصال بقاعدة البيانات مباشرة هنا
            connection = sqlite3.connect('students.db')
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO students (id,name, branch, contact) 
                              VALUES (?,?, ?, ?)''', 
                           (student_id,student_name, branch_name, contact_number))
            connection.commit()
            connection.close()
            
            messagebox.showinfo("Success", "Student has been added successfully!")
            
            # مسح الحقول بعد الإضافة
            entry_student_id.delete(0, tk.END)
            entry_student_name.delete(0, tk.END)
            entry_branch_name.delete(0, tk.END)
            entry_contact_number.delete(0, tk.END)
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while saving to the database: {e}")


    def save_book():
        # استرجاع القيم من الإدخالات
        book_id = entry_book_id_add.get()
        book_title = entry_book_title.get()
        author = entry_author.get()
        genre = entry_genre.get()
        copies = entry_copies.get()
        
        # التحقق من صحة المدخلات
        if not book_id or not book_title or not author or not genre or not copies:
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        if not book_id.isdigit() or not copies.isdigit():
            messagebox.showerror("Input Error", "Book ID and Copies must be numeric values.")
            return
        if not isinstance(author, str) or not author.replace(" ", "").isalpha():
            messagebox.showerror("Input Error", "author must be a valid string containing only letters.")
            return
        
        if not isinstance(genre, str) or not genre.replace(" ", "").isalpha():
            messagebox.showerror("Input Error", "genre must be a valid string containing only letters.")
            return
        
        # الاتصال بقاعدة البيانات
        db = sqlite3.connect("books.db")
        cr = db.cursor()
    
        # التحقق إذا كان الكتاب موجودًا بالفعل في قاعدة البيانات
        cr.execute("SELECT copies FROM books WHERE book_id = ?", (book_id,))
        existing_book = cr.fetchone()
    
        if existing_book:
            # إذا كان الكتاب موجودًا، قم بزيادة عدد النسخ
            new_copies = existing_book[0] + int(copies)
            cr.execute("UPDATE books SET copies = ? WHERE book_id = ?", (new_copies, book_id))
            messagebox.showinfo("Success", f"Copies updated. New copy count: {new_copies}")
        else:
            # إذا لم يكن الكتاب موجودًا، أضفه إلى قاعدة البيانات
            cr.execute("INSERT INTO books (book_id, book_title, author, genre, copies) VALUES (?, ?, ?, ?, ?)",
                       (book_id, book_title, author, genre, int(copies)))
            messagebox.showinfo("Success", "The book has been added successfully!")
    
        # حفظ التغييرات
        db.commit()
        db.close()
        
        # مسح الحقول
        entry_book_id_add.delete(0, tk.END)
        entry_book_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        entry_copies.delete(0, tk.END)
    

# دالة لحفظ الاستعارة
    def save_borrow():
        student_id = entry_student_id.get()
        book_id = entry_book_id.get()
        issue_date = entry_issue_date.get()
        return_date = entry_return_date.get()
    
        # التحقق من صحة البيانات
        if not student_id.strip() or not book_id.strip() or not issue_date.strip() or not return_date.strip():
            messagebox.showerror("Input Error", "All fields are required!")
            return
    
        # التحقق من أن book_id رقمي
        if not book_id.isdigit():
            messagebox.showerror("Input Error", "Book ID must be a numeric value.")
            return
    
        # التحقق من أن student_id موجود في قاعدة البيانات
        try:
            with sqlite3.connect("students.db") as student_db:
                student_cursor = student_db.cursor()
                student_cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
                student = student_cursor.fetchone()
                if not student:
                    messagebox.showerror("Student Not Found", "No student found with the provided ID.")
                    return
    
            # الاتصال بقاعدة البيانات للكتب
            with sqlite3.connect("books.db") as db:
                cr_books = db.cursor()
    
                # الاتصال بقاعدة البيانات للمعاملات
                with sqlite3.connect('transactions.db') as tr:
                    cr_transactions = tr.cursor()
    
                    # التحقق من وجود الكتاب في قاعدة البيانات
                    cr_books.execute("SELECT book_title, copies FROM books WHERE book_id = ?", (book_id,))
                    book = cr_books.fetchone()
    
                    if not book:
                        messagebox.showerror("Book Not Found", "No book found with the provided ID.")
                        return
    
                    book_title, copies = book
    
                    # التحقق من توفر نسخ الكتاب
                    if copies <= 0:
                        messagebox.showerror("Unavailable", "The book is currently unavailable for borrowing.")
                        return
    
                    # التحقق من أن تاريخ الاستعارة هو تاريخ اليوم فقط
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    if issue_date != today:
                        messagebox.showerror("Date Error", "The issue date must be today's date.")
                        return
    
                    # التحقق من أن تاريخ الإرجاع صالح
                    def validate_date(date_str):
                        """
                        يتحقق مما إذا كان النص المدخل يمثل تاريخًا صالحًا بالتنسيق YYYY-MM-DD.
                        """
                        try:
                            datetime.datetime.strptime(date_str, "%Y-%m-%d")
                            return True
                        except ValueError:
                            return False
    
                    if not validate_date(return_date):
                        messagebox.showerror("Invalid Date", "Please enter a valid return date in the format YYYY-MM-DD.")
                        return
    
                    # التحقق من أن تاريخ الإرجاع ليس في الماضي
                    if datetime.datetime.strptime(return_date, "%Y-%m-%d") < datetime.datetime.strptime(today, "%Y-%m-%d"):
                        messagebox.showerror("Date Error", "The return date cannot be in the past.")
                        return
    
                    # تقليل عدد النسخ في قاعدة البيانات
                    updated_copies = copies - 1
                    cr_books.execute("UPDATE books SET copies = ? WHERE book_id = ?", (updated_copies, book_id))
                    db.commit()
    
                    # إضافة المعاملة إلى قاعدة بيانات المعاملات
                    cr_transactions.execute(
                        "INSERT INTO transactions (student_id, book_id, date_borrowed, date_returned) VALUES (?, ?, ?, ?)",
                        (student_id, book_id, issue_date, return_date)
                    )
                    tr.commit()
    
                    # عرض رسالة النجاح بعد التأكد من صحة البيانات
                    messagebox.showinfo("Success", "The book has been borrowed successfully!")
    
                    # مسح الحقول
                    entry_student_id.delete(0, tk.END)
                    entry_book_id.delete(0, tk.END)
                    entry_issue_date.delete(0, tk.END)
                    entry_return_date.delete(0, tk.END)
    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            print(f"Database error: {e}")
    

  
    def return_book():
            book_id = entry_return_book_id.get()
            student_id = entry_return_student_id.get()
            return_date = entry_return_date.get()
        
            # التحقق من صحة البيانات المدخلة
            if not book_id.strip() or not student_id.strip() or not return_date.strip():
                messagebox.showerror("Input Error", "All fields are required!")
                return
        
            try:
                # الاتصال بقاعدة بيانات المعاملات
                tr = sqlite3.connect('transactions.db')
                cr_transactions = tr.cursor()
                
                # التحقق من وجود المعاملة وجلب جميع البيانات بناءً على book_id و student_id
                cr_transactions.execute(
                    """
                    SELECT * 
                    FROM transactions 
                    WHERE book_id = ? AND student_id = ? 
                    """,
                    (book_id, student_id)
                )
                transaction = cr_transactions.fetchall()
        
                # التحقق من أن المعاملة موجودة
                if not transaction:
                    messagebox.showerror("Not Found", "No active transaction found for the provided book ID and student ID.")
                    return
                # إغلاق الاتصال بقاعدة البيانات
                tr.close()
        
                # التحقق من أن تاريخ الإرجاع صالح
                def validate_date(date_str):
                    """
                    يتحقق مما إذا كان النص المدخل يمثل تاريخًا صالحًا بالتنسيق YYYY-MM-DD.
                    """
                    try:
                        datetime.datetime.strptime(date_str, "%Y-%m-%d")
                        return True
                    except ValueError:
                        return False
        
                if not validate_date(return_date):
                    messagebox.showerror("Invalid Date", "Please enter a valid return date in the format YYYY-MM-DD.")
                    return
                    
                 # التحقق من أن تاريخ الإرجاع ليس في الماضي
                try:
                    input_date = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
                    if input_date < datetime.date.today() :
                        messagebox.showerror("Invalid Date", "Return date cannot be in the past!")
                        return
                    if input_date > datetime.date.today() :
                        messagebox.showerror("Invalid Date", "Return date cannot be in the future!")
                        return
                except ValueError:
                    messagebox.showerror("Invalid Date", "Please enter a valid return date in the format YYYY-MM-DD.")
                    return
                # حذف المعاملة من جدول المعاملات
                tr = sqlite3.connect('transactions.db')
                cr_transactions = tr.cursor()
                cr_transactions.execute("DELETE FROM transactions WHERE book_id = ? AND student_id = ?", (book_id, student_id))
                tr.commit()
                
                # زيادة عدد النسخ في جدول الكتب
                db = sqlite3.connect("books.db")
                cr_books = db.cursor()
        
                cr_books.execute("UPDATE books SET copies = copies + 1 WHERE book_id = ?", (book_id,))
                db.commit()
                db.close()
        
                # عرض رسالة نجاح
                messagebox.showinfo("Success", "The book has been successfully returned and the transaction removed!")
        
                # مسح الحقول
                entry_return_book_id.delete(0, tk.END)
                entry_return_student_id.delete(0, tk.END)
                entry_return_date.delete(0, tk.END)
        
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
                print(f"Database error: {e}")
        
            finally:
                # إغلاق الاتصال بقاعدة البيانات
                if 'tr' in locals() and tr:
                    tr.close()
                if 'db' in locals() and db:
                    db.close()
    
         
          # دالة لعرض الكتب من قاعدة البيانات
    def display_books():
# مسح جميع الأدوات الحالية داخل عنصر content
        for widget in content.winfo_children():
            widget.destroy()
    
        # إنشاء إطار الجدول
        table_frame = ttk.Frame(content, relief="ridge", borderwidth=2)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
        # عنوان الجدول
        title_label = ttk.Label(table_frame, text="View Books", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
    
        # إنشاء جدول Treeview مع شريط تمرير
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True, pady=10)
    
        # إضافة شريط تمرير (Scrollbar)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
    
        # إنشاء Treeview
        tree = ttk.Treeview(tree_frame, columns=("Book ID", "Book Title", "Author", "Genre", "Copies"), show="headings", yscrollcommand=scrollbar.set)
        tree.pack(fill="both", expand=True)
    
        scrollbar.config(command=tree.yview)
    
        # إعداد رؤوس الأعمدة
        tree.heading("Book ID", text="Book ID")
        tree.heading("Book Title", text="Book Title")
        tree.heading("Author", text="Author")
        tree.heading("Genre", text="Genre")
        tree.heading("Copies", text="Copies")
    
        # ضبط عرض الأعمدة
        for col in ("Book ID", "Book Title", "Author", "Genre", "Copies"):
            tree.column(col, width=150, anchor="center")
    
        # استرجاع البيانات من قاعدة البيانات
        try:
            db = sqlite3.connect("books.db")
            cr = db.cursor()
            cr.execute("SELECT * FROM books")
            rows = cr.fetchall()
            db.close()
    
            # إدخال البيانات في الجدول
            for row in rows:
                tree.insert("", "end", values=row)
    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            print(f"Database error: {e}")
    
        # عرض الجدول في واجهة المستخدم
        tree.pack(pady=20, fill=tk.BOTH, expand=True)
        tree.bind("<Double-1>", lambda event: open_book_details(event, tree))
    def open_book_details(event, tree):
        # الحصول على البيانات من الصف الذي تم الضغط عليه
        item = tree.selection()[0]  # تحديد الصف الذي تم اختياره
        book_id, title, author, genre, copies = tree.item(item, 'values')
        
        # فتح نافذة جديدة لتعديل بيانات الكتاب
        edit_window = tk.Toplevel()
        edit_window.title(f"Edit Book - {title}")
        edit_window.geometry("400x400")
    
        # حقول الإدخال لتعديل بيانات الكتاب
        tk.Label(edit_window, text="Book Title:").pack(pady=5)
        entry_title = tk.Entry(edit_window, font=("Arial", 12))
        entry_title.insert(0, title)
        entry_title.pack(pady=5)
    
        tk.Label(edit_window, text="Author:").pack(pady=5)
        entry_author = tk.Entry(edit_window, font=("Arial", 12))
        entry_author.insert(0, author)
        entry_author.pack(pady=5)
    
        tk.Label(edit_window, text="Genre:").pack(pady=5)
        entry_genre = tk.Entry(edit_window, font=("Arial", 12))
        entry_genre.insert(0, genre)
        entry_genre.pack(pady=5)
    
        tk.Label(edit_window, text="Copies:").pack(pady=5)
        entry_copies = tk.Entry(edit_window, font=("Arial", 12))
        entry_copies.insert(0, copies)
        entry_copies.pack(pady=5)
    
        def save_changes():
            new_title = entry_title.get()
            new_author = entry_author.get()
            new_genre = entry_genre.get()
            new_copies = entry_copies.get()
    
            # التحقق من صحة البيانات
            if not new_title or not new_author or not new_genre or not new_copies.isdigit():
                messagebox.showerror("Error", "All fields must be filled correctly!")
                return
            
            # تحديث قاعدة البيانات بالبيانات الجديدة
            db = sqlite3.connect("books.db")
            cr = db.cursor()
            cr.execute("""
                UPDATE books
                SET book_title = ?, author = ?, genre = ?, copies = ?
                WHERE book_id = ?
            """, (new_title, new_author, new_genre, int(new_copies), book_id))
            db.commit()
            db.close()
    
            # إغلاق نافذة التعديل
            edit_window.destroy()
    
            # تحديث الجدول في النافذة الرئيسية
            display_books()
            messagebox.showinfo("Success", "Book details updated successfully.")
    
        def delete_book():
            # تأكيد الحذف
            confirm = messagebox.askyesno("Delete Book", "Are you sure you want to delete this book?")
            if confirm:
                db = sqlite3.connect("books.db")
                cr = db.cursor()
                cr.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
                db.commit()
                db.close()
    
                # إغلاق نافذة التعديل
                edit_window.destroy()
    
                # تحديث الجدول في النافذة الرئيسية
                display_books()
                messagebox.showinfo("Success", "Book deleted successfully.")
    
        # إضافة زر لحفظ التغييرات
        tk.Button(edit_window, text="Save Changes", font=("Arial", 12), bg="#6f42c1", fg="white", command=save_changes).pack(pady=10)
        
        # إضافة زر لحذف الكتاب
        tk.Button(edit_window, text="Delete Book", font=("Arial", 12), bg="red", fg="white", command=delete_book).pack(pady=10)
    
        # زر لغلق النافذة
        tk.Button(edit_window, text="Close", font=("Arial", 12), bg="gray", fg="white", command=edit_window.destroy).pack(pady=10)
    
       


    # دالة لحساب الأيام المتأخرة
    # دالة لحساب الأيام المتأخرة
    def calculate_days_late(date_borrowed, date_returned):
        today = datetime.date.today()
        
        if date_returned:
            # إذا تم إرجاع الكتاب
            if date_returned < today:
                # إذا كان تاريخ الإرجاع أقل من تاريخ اليوم
                return (today - date_returned).days
            else:
                return 0  # إذا كان الكتاب تم إرجاعه في المستقبل (غالباً غير متوقع)
        else:
            # إذا لم يتم إرجاع الكتاب بعد
            return 0  # لا يتم حساب الأيام المتأخرة إذا لم يتم الإرجاع حتى اليوم الحالي
    
#     دالة لعرض المعاملات
    def display_transactions(content):
        # مسح جميع الأدوات الحالية داخل عنصر content
        for widget in content.winfo_children():
            widget.destroy()
    
        # إنشاء إطار الجدول بحجم أكبر
        table_frame = ttk.Frame(content, relief="ridge", borderwidth=2)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
        # عنوان الجدول
        title_label = ttk.Label(table_frame, text="View Transactions", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
    
        # إنشاء جدول Treeview مع شريط تمرير
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True, pady=10)
    
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
    
        tree = ttk.Treeview(tree_frame, columns=("Student ID", "Book ID", "Date Borrowed", "Date Returned", "Days Late"), show="headings", yscrollcommand=scrollbar.set)
        tree.pack(fill="both", expand=True)
    
        scrollbar.config(command=tree.yview)
    
        # إعداد رؤوس الأعمدة
        tree.heading("Student ID", text="Student ID")
        tree.heading("Book ID", text="Book ID")
        tree.heading("Date Borrowed", text="Date Borrowed")
        tree.heading("Date Returned", text="Date Returned")
        tree.heading("Days Late", text="Days Late")
    
        # ضبط عرض الأعمدة
        for col in ("Student ID", "Book ID", "Date Borrowed", "Date Returned", "Days Late"):
            tree.column(col, width=150, anchor="center")
    
        # الاتصال بقاعدة البيانات وجلب المعاملات
        try:
            conn = sqlite3.connect('transactions.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions')
            transactions = cursor.fetchall()
            conn.close()
    
            # إدراج البيانات في الجدول
            for transaction in transactions:
                student_id = transaction[1]
                book_id = transaction[2]
                date_borrowed = datetime.datetime.strptime(transaction[3], "%Y-%m-%d").date()
                date_returned = datetime.datetime.strptime(transaction[4], "%Y-%m-%d").date() if transaction[4] else None
    
                # حساب الأيام المتأخرة
                days_late = calculate_days_late(date_borrowed, date_returned)
    
                # إدراج البيانات في الجدول
                tree.insert("", "end", values=(
                    student_id,
                    book_id,
                    date_borrowed.strftime("%Y-%m-%d"),
                    transaction[4] if transaction[4] else "Not Returned",
                    days_late if days_late > 0 else "-"
                ))
    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            print(f"Database error: {e}")
            
            
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("1000x600")
    root.configure(bg="#f8f9fa")
    
    # جعل النافذة ملء الشاشة
    root.attributes("-fullscreen", True)
    
    # Sidebar
    sidebar = tk.Frame(root, width=200, height=400, bg="#6f42c1")
    sidebar.pack(side="left", fill="y")
    
    # Open the image using PIL
    image_path = r"D:\PYthon projects\Final Project LMS\rb_2148608688[1].png"
    img = Image.open(image_path)
    img = img.resize((150, 150))  # Resize the image to fit in the label if needed
    img = ImageTk.PhotoImage(img)
    
    # Create a label to display the image
    logo = tk.Label(sidebar, image=img, bg="#6f42c1")
    logo.image = img  # Keep a reference to the image to avoid garbage collection
    logo.pack(pady=20)
    
    

    # Function to create buttons in the sidebar with hover effect
    def create_sidebar_button(text, command):
        def on_enter(event):
            button.config(bg="#5a35a1")  # لون عند تحريك الماوس
    
        def on_leave(event):
            button.config(bg="#6f42c1")  # اللون الافتراضي
    
        button = tk.Button(sidebar, text=text, bg="#6f42c1", fg="white", bd=2, relief="raised", pady=10,
                           highlightthickness=0, font=("Arial", 12, "bold"), command=command)
        button.bind("<Enter>", on_enter)  # عند مرور الماوس
        button.bind("<Leave>", on_leave)  # عند مغادرة الماوس
        return button
        

    btn_add_student = create_sidebar_button("Add Student", lambda: switch_to_add_student())
    btn_add_student.pack(fill=tk.X, pady=13)

    btn_add_book = create_sidebar_button("Add Book", lambda: switch_to_add_book())
    btn_add_book.pack(fill=tk.X, pady=13)

    btn_issue_book_sidebar = create_sidebar_button("Issue Book", lambda: switch_to_issue_book(content))
    btn_issue_book_sidebar.pack(fill=tk.X, pady=13)

    btn_return_book = create_sidebar_button("Return Book", lambda: switch_to_return_book(content))
    btn_return_book.pack(fill=tk.X, pady=13)

    btn_search_book = create_sidebar_button("Search Book", lambda: switch_to_search_boo(content))
    btn_search_book.pack(fill=tk.X, pady=13)
    # New Buttons
    btn_search_student = create_sidebar_button("Search Student", lambda: switch_to_search_student(content))
    btn_search_student.pack(fill=tk.X, pady=13)

    btn_view_books = create_sidebar_button("View Books", display_books)
    btn_view_books.pack(fill=tk.X, pady=13)
    btn_transactions = create_sidebar_button("Transactions", lambda:display_transactions(content))
    btn_transactions.pack(fill=tk.X, pady=13)
    
    
    
    btn_exit = create_sidebar_button("Exit", lambda: root.destroy())
    btn_exit.pack(fill=tk.X, pady=13)
    
    # Main Content
    content = tk.Frame(root, bg="#f8f9fa")
    content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    # Load and display image
    image_path = r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # حدد مسار الصورة هنا
    try:
        img = Image.open(image_path)  # تحميل الصورة
        img = img.resize((1500, 1000))  # تعديل حجم الصورة
        photo = ImageTk.PhotoImage(img)  # تحويل الصورة إلى شكل يمكن استخدامها في Tkinter
        
        image_label = tk.Label(content, image=photo, bg="#f8f9fa")  # إنشاء التصنيف الذي يعرض الصورة
        image_label.image = photo  # الاحتفاظ بالمرجع للصورة (لتجنب فقدانها)
        image_label.pack(pady=0)  # عرض الصورة
    except Exception as e:
        error_label = tk.Label(content, text="Error loading image.", fg="red", bg="#f8f9fa", font=("Arial", 16))
        error_label.pack(pady=20)


    def switch_to_add_student():
         for widget in content.winfo_children():
             
             widget.destroy()
        
                 # تحميل الصورة وتعيينها كخلفية
         try:
             bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
             bg_img = Image.open(bg_image_path)
             bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
             bg_photo = ImageTk.PhotoImage(bg_img)
     
             # وضع الصورة كخلفية
             bg_label = tk.Label(content, image=bg_photo)
             bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
             bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
         except Exception as e:
             print(f"Error loading background image: {e}")
        
         # عنوان رئيسي
         header_label = tk.Label(content, text="Add Student", font=("Arial", 24, "bold"), bg="#f8f9fa")
         header_label.pack(pady=20)
        
         # إطار النموذج
         form_frame = tk.Frame(content, bg="white", padx=30, pady=30, relief=tk.RIDGE, bd=2 ,)
         form_frame.pack(pady=20)
        
         global entry_student_id, entry_student_name, entry_branch_name, entry_contact_number
        
         # تعريف الحقول والعناوين مع زيادة حجم الخط والمسافات
         label_student_id = tk.Label(form_frame, text="Student ID", bg="white", font=("Arial", 16))
         label_student_id.grid(row=0, column=0, padx=15, pady=15, sticky=tk.W)
         entry_student_id = tk.Entry(form_frame, font=("Arial", 16), width=30)  # زيادة حجم الحقل
         entry_student_id.grid(row=0, column=1, padx=15, pady=15)
        
         label_student_name = tk.Label(form_frame, text="Student Name", bg="white", font=("Arial", 16))
         label_student_name.grid(row=1, column=0, padx=15, pady=15, sticky=tk.W)
         entry_student_name = tk.Entry(form_frame, font=("Arial", 16), width=30)  # زيادة حجم الحقل
         entry_student_name.grid(row=1, column=1, padx=15, pady=15)
        
         label_branch_name = tk.Label(form_frame, text="Branch Name", bg="white", font=("Arial", 16))
         label_branch_name.grid(row=2, column=0, padx=15, pady=15, sticky=tk.W)
         entry_branch_name = tk.Entry(form_frame, font=("Arial", 16), width=30)  # زيادة حجم الحقل
         entry_branch_name.grid(row=2, column=1, padx=15, pady=15)
        
         label_contact_number = tk.Label(form_frame, text="Contact Number", bg="white", font=("Arial", 16))
         label_contact_number.grid(row=3, column=0, padx=15, pady=15, sticky=tk.W)
         entry_contact_number = tk.Entry(form_frame, font=("Arial", 16), width=30)  # زيادة حجم الحقل
         entry_contact_number.grid(row=3, column=1, padx=15, pady=15)
        
         # زر الإرسال مع حجم أكبر
         submit_btn = tk.Button(content, text="Save Student", font=("Arial", 18), bg="#6A1B9A", fg="white",
                                width=20, height=2, command=save_student)  # زيادة حجم الزر
         submit_btn.pack(pady=20)

    def switch_to_add_book():
        # إزالة جميع المكونات الحالية من المحتوى
        for widget in content.winfo_children():
            widget.destroy()
    
        # تحميل الصورة وتعيينها كخلفية
        try:
            bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
            bg_img = Image.open(bg_image_path)
            bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
            bg_photo = ImageTk.PhotoImage(bg_img)
    
            # وضع الصورة كخلفية
            bg_label = tk.Label(content, image=bg_photo)
            bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
        except Exception as e:
            print(f"Error loading background image: {e}")
    
        # إنشاء المكونات فوق الخلفية
        header_label = tk.Label(content, text="Add Book", font=("Arial", 24, "bold"), bg="#f8f9fa")
        header_label.pack(pady=20)
    
        form_frame = tk.Frame(content, bg="white", padx=30, pady=30, relief=tk.RIDGE, bd=2)
        form_frame.pack(pady=20)
    
        global entry_book_id_add, entry_book_title, entry_author, entry_genre, entry_copies
    
        # تعريف الحقول والعناوين مع زيادة حجم الخط والمسافات
        label_book_id = tk.Label(form_frame, text="Book ID", bg="white", font=("Arial", 16))
        label_book_id.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)
        entry_book_id_add = tk.Entry(form_frame, font=("Arial", 16), width=40)  # زيادة حجم الحقل
        entry_book_id_add.grid(row=0, column=1, padx=20, pady=20)
    
        label_book_title = tk.Label(form_frame, text="Book Title", bg="white", font=("Arial", 16))
        label_book_title.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W)
        entry_book_title = tk.Entry(form_frame, font=("Arial", 16), width=40)  # زيادة حجم الحقل
        entry_book_title.grid(row=1, column=1, padx=20, pady=20)
    
        label_author = tk.Label(form_frame, text="Author", bg="white", font=("Arial", 16))
        label_author.grid(row=2, column=0, padx=20, pady=20, sticky=tk.W)
        entry_author = tk.Entry(form_frame, font=("Arial", 16), width=40)  # زيادة حجم الحقل
        entry_author.grid(row=2, column=1, padx=20, pady=20)
    
        label_genre = tk.Label(form_frame, text="Genre", bg="white", font=("Arial", 16))
        label_genre.grid(row=3, column=0, padx=20, pady=20, sticky=tk.W)
        entry_genre = tk.Entry(form_frame, font=("Arial", 16), width=40)  # زيادة حجم الحقل
        entry_genre.grid(row=3, column=1, padx=20, pady=20)
    
        # حقل جديد لعدد النسخ
        label_copies = tk.Label(form_frame, text="Number of Copies", bg="white", font=("Arial", 16))
        label_copies.grid(row=4, column=0, padx=20, pady=20, sticky=tk.W)
        entry_copies = tk.Entry(form_frame, font=("Arial", 16), width=40)  # زيادة حجم الحقل
        entry_copies.grid(row=4, column=1, padx=20, pady=20)
    
        # زر حفظ الكتاب مع حجم أكبر
        submit_btn = tk.Button(content, text="Save Book", font=("Arial", 18), bg="#6A1B9A", fg="white", width=20, height=2, command=save_book)
        submit_btn.pack(pady=20)
    
                
    # Add more functions for issue, return, search books here...
    ##33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
    def switch_to_issue_book(content):
        # مسح المحتوى الحالي
        for widget in content.winfo_children():
            widget.destroy()
        
                        # تحميل الصورة وتعيينها كخلفية
        try:
            bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
            bg_img = Image.open(bg_image_path)
            bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
            bg_photo = ImageTk.PhotoImage(bg_img)
       
            # وضع الصورة كخلفية
            bg_label = tk.Label(content, image=bg_photo)
            bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
        except Exception as e:
            print(f"Error loading background image: {e}")
        
        
        # العنوان
        header_label = tk.Label(content, text="Borrow a Book", font=("Arial", 24, "bold"), bg="#f8f9fa")
        header_label.pack(pady=20)

        # إطار الحقول
        form_frame = tk.Frame(content, bg="white", padx=30, pady=30, relief=tk.RIDGE, bd=2)
        form_frame.pack(pady=20)
        
        global entry_student_id, entry_book_id, entry_issue_date, entry_return_date

        # Student ID
        label_student_id = tk.Label(form_frame, text="Student ID", bg="white", font=("Arial", 16))
        label_student_id.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)
        entry_student_id = tk.Entry(form_frame, font=("Arial", 16))
        entry_student_id.grid(row=0, column=1, padx=20, pady=20)

        # Book ID
        label_book_id = tk.Label(form_frame, text="Book ID", bg="white", font=("Arial", 16))
        label_book_id.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W)
        entry_book_id = tk.Entry(form_frame, font=("Arial", 16))
        entry_book_id.grid(row=1, column=1, padx=20, pady=20)

        # Issue Date
        label_issue_date = tk.Label(form_frame, text="Issue Date (YYYY-MM-DD)", bg="white", font=("Arial", 16))
        label_issue_date.grid(row=2, column=0, padx=20, pady=20, sticky=tk.W)
        entry_issue_date = tk.Entry(form_frame, font=("Arial", 16))
        entry_issue_date.grid(row=2, column=1, padx=20, pady=20)

        # Return Date
        label_return_date = tk.Label(form_frame, text="Return Date (YYYY-MM-DD)", bg="white", font=("Arial", 16))
        label_return_date.grid(row=3, column=0, padx=20, pady=20, sticky=tk.W)
        entry_return_date = tk.Entry(form_frame, font=("Arial", 16))
        entry_return_date.grid(row=3, column=1, padx=20, pady=20)

        # زر الاستعارة
        borrow_button = tk.Button( content , text="Borrow Book",  font=("Arial", 18), bg="#6A1B9A", fg="white", width=20, height=2, command=save_borrow)
        
           
        borrow_button.pack(pady=20)
        on_focus_issue_date()
        




 # دالة للتحديث التلقائي لتاريخ الاستعارة عند تحميل النموذج
    # دالة للتحديث التلقائي لتاريخ الاستعارة عند تحميل النموذج
    def on_focus_issue_date():
        today = datetime.datetime.now()
        issue_date = today.strftime("%Y-%m-%d")  # الحصول على تاريخ اليوم
        entry_issue_date.delete(0, tk.END)
        entry_issue_date.insert(0, issue_date)  # 


# دالة للتحديث التلقائي لتاريخ الإرجاع بعد تاريخ الاستعارة
    
    def switch_to_return_book(content):
        # مسح المحتوى الحالي
        for widget in content.winfo_children():
            widget.destroy()
 
                                # تحميل الصورة وتعيينها كخلفية
        try:
            bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
            bg_img = Image.open(bg_image_path)
            bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
            bg_photo = ImageTk.PhotoImage(bg_img)
       
            # وضع الصورة كخلفية
            bg_label = tk.Label(content, image=bg_photo)
            bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
        except Exception as e:
            print(f"Error loading background image: {e}")
        
        header_label = tk.Label(content, text="Return Book", font=("Arial", 24, "bold"), bg="#f8f9fa")
        header_label.pack(pady=20)

        form_frame = tk.Frame(content, bg="white", padx=30, pady=30, relief=tk.RIDGE, bd=2)
        form_frame.pack(pady=20)

        global entry_return_book_id, entry_return_student_id, entry_return_date

        label_return_book_id = tk.Label(form_frame, text="Book ID", bg="white", font=("Arial", 16))
        label_return_book_id.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)
        entry_return_book_id = tk.Entry(form_frame, font=("Arial", 16))
        entry_return_book_id.grid(row=0, column=1, padx=20, pady=20)

        label_return_student_id = tk.Label(form_frame, text="Student ID", bg="white", font=("Arial", 16))
        label_return_student_id.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W)
        entry_return_student_id = tk.Entry(form_frame, font=("Arial", 16))
        entry_return_student_id.grid(row=1, column=1, padx=20, pady=20)

        label_return_date = tk.Label(form_frame, text="Return Date", bg="white", font=("Arial", 16))
        label_return_date.grid(row=2, column=0, padx=20, pady=20, sticky=tk.W)
        entry_return_date = tk.Entry(form_frame, font=("Arial", 16))
        entry_return_date.grid(row=2, column=1, padx=20, pady=20)

        submit_btn = tk.Button(content, text="Return Book", font=("Arial", 18), bg="#6A1B9A", fg="white", width=20, height=2,
                               command=return_book)
        submit_btn.pack(pady=20)


# --------------------------------------------------------------------------------------------------------
# دالة لعرض واجهة البحث
def switch_to_search_boo(content):
    for widget in content.winfo_children():
        widget.destroy()
    
                            # تحميل الصورة وتعيينها كخلفية
        try:
            bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
            bg_img = Image.open(bg_image_path)
            bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
            bg_photo = ImageTk.PhotoImage(bg_img)
       
            # وضع الصورة كخلفية
            bg_label = tk.Label(content, image=bg_photo)
            bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
        except Exception as e:
            print(f"Error loading background image: {e}")
    
    # إضافة العنوان
    header_label = tk.Label(content, text="Search Book", font=("Arial", 18, "bold"), bg="#f8f9fa")
    header_label.pack(pady=20)

    form_frame = tk.Frame(content, bg="white", padx=30, pady=30, relief=tk.RIDGE, bd=2)
    form_frame.pack(pady=20)

    # إضافة Label فوق حقل الإدخال
    label_search = tk.Label(form_frame, text="Enter ID / Book Name / Author / Genre:", bg="white", font=("Arial", 16))
    label_search.grid(row=0, column=0, padx=20, pady=20)

    # حقل الإدخال
    entry_search_query = tk.Entry(form_frame, font=("Arial", 16), width=40)
    entry_search_query.grid(row=1, column=0, padx=20, pady=20)

    # زر البحث
    search_button = tk.Button(content, text="Search", font=("Arial", 18), bg="#6A1B9A", fg="white",
                              command=lambda: search_book(entry_search_query.get(), content))
    search_button.pack(pady=20)

def search_book(query, content):
    # التحقق إذا كان الحقل فارغًا
                        # تحميل الصورة وتعيينها كخلفية
    try:
        bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
        bg_img = Image.open(bg_image_path)
        bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
        bg_photo = ImageTk.PhotoImage(bg_img)
   
        # وضع الصورة كخلفية
        bg_label = tk.Label(content, image=bg_photo)
        bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
    except Exception as e:
        print(f"Error loading background image: {e}")
    
    
    
    if not query.strip():
        messagebox.showerror("Input Error", "The search field cannot be empty.")
        return

    try:
        # الاتصال بقاعدة بيانات الكتب
        db = sqlite3.connect("books.db")
        cr = db.cursor()

        # تنفيذ استعلام البحث عن الكتب باستخدام تطابق دقيق للكلمة الكاملة
        cr.execute("""
            SELECT * FROM books 
            WHERE book_title = ? OR author = ? OR genre = ? OR book_id = ?
        """, 
        (query, query, query, query))

        # جلب جميع النتائج
        results = cr.fetchall()

        # إذا تم العثور على نتائج
        if results:
            # تحويل النتائج إلى تنسيق يمكن عرضه في واجهة المستخدم
            books = []
            for row in results:
                book = {
                    "id": row[0],
                    "title": row[1],
                    "author": row[2],
                    "genre": row[3],
                    "copies": row[4]
                }
                books.append(book)
            display_search_results(books, content)
        else:
            # إذا لم يتم العثور على أي كتب
            messagebox.showinfo("No Results", "No books found matching the query.")
        

        # إغلاق الاتصال بقاعدة البيانات
        db.close()

    except sqlite3.Error as e:
        # عرض رسالة خطأ إذا حدثت مشكلة في الاتصال بقاعدة البيانات
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        print(f"Database error: {e}")
def display_search_results(results, content):
    # مسح العناصر السابقة إذا وجدت 
                            # تحميل الصورة وتعيينها كخلفية
    try:
        bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
        bg_img = Image.open(bg_image_path)
        bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
        bg_photo = ImageTk.PhotoImage(bg_img)
   
        # وضع الصورة كخلفية
        bg_label = tk.Label(content, image=bg_photo)
        bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
    except Exception as e:
        print(f"Error loading background image: {e}")
    
    
    
    for widget in content.winfo_children():
        widget.destroy()
    
    table_frame = tk.Frame(content, bg="white", padx=20, pady=20, relief=tk.RIDGE, bd=2)
    table_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
    
    # عنوان النتائج
    header_label = tk.Label(
        table_frame, text="Search Results", font=("Arial", 18, "bold"), bg="#f8f9fa"
    )
    header_label.pack(pady=10)
    
    # إنشاء Treeview لعرض النتائج
    tree = ttk.Treeview(
        table_frame, 
        columns=("ID", "Title", "Author", "Genre", "Copies"), 
        show="headings", 
        height=8
    )
    
    # تحديد رؤوس الأعمدة
    tree.heading("ID", text="Book ID")
    tree.heading("Title", text="Book Title")
    tree.heading("Author", text="Author")
    tree.heading("Genre", text="Genre")
    tree.heading("Copies", text="Copies")
    
    # تحديد عرض الأعمدة
    tree.column("ID", width=80, anchor="center")
    tree.column("Title", width=180, anchor="w")
    tree.column("Author", width=140, anchor="w")
    tree.column("Genre", width=90, anchor="w")
    tree.column("Copies", width=80, anchor="center")
    
    # إضافة البيانات إلى Treeview
    for book in results:
        tree.insert("", "end", values=(book["id"], book["title"], book["author"], book["genre"], book["copies"]))
    
    # إضافة Treeview إلى واجهة المستخدم
    tree.pack(pady=10, fill="both", expand=True)
    
    # عند الضغط المزدوج على صف
    tree.bind("<Double-1>", lambda event: open_book_details(event, tree, results, content))

def open_book_details(event, tree, results, content):
    # الحصول على البيانات من الصف الذي تم الضغط عليه
    selected_item = tree.selection()[0]
    book_id, title, author, genre, copies = tree.item(selected_item, 'values')
    
    # نافذة تعديل بيانات الكتاب
    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Book - {title}")
    edit_window.geometry("400x400")
    
    # إدخال البيانات لتعديلها
    tk.Label(edit_window, text="Book Title:").pack(pady=5)
    entry_title = tk.Entry(edit_window, font=("Arial", 12))
    entry_title.insert(0, title)
    entry_title.pack(pady=5)
    
    tk.Label(edit_window, text="Author:").pack(pady=5)
    entry_author = tk.Entry(edit_window, font=("Arial", 12))
    entry_author.insert(0, author)
    entry_author.pack(pady=5)
    
    tk.Label(edit_window, text="Genre:").pack(pady=5)
    entry_genre = tk.Entry(edit_window, font=("Arial", 12))
    entry_genre.insert(0, genre)
    entry_genre.pack(pady=5)
    
    tk.Label(edit_window, text="Copies:").pack(pady=5)
    entry_copies = tk.Entry(edit_window, font=("Arial", 12))
    entry_copies.insert(0, copies)
    entry_copies.pack(pady=5)
    
    def save_changes():
        new_title = entry_title.get()
        new_author = entry_author.get()
        new_genre = entry_genre.get()
        new_copies = entry_copies.get()
        
        if not new_title or not new_author or not new_genre or not new_copies.isdigit():
            messagebox.showerror("Error", "All fields must be filled correctly!")
            return
        
        # تحديث قاعدة البيانات
        db = sqlite3.connect("books.db")
        cr = db.cursor()
        cr.execute("""
            UPDATE books
            SET book_title = ?, author = ?, genre = ?, copies = ?
            WHERE book_id = ?
        """, (new_title, new_author, new_genre, int(new_copies), book_id))
        db.commit()
        db.close()
        
        edit_window.destroy()
        messagebox.showinfo("Success", "Book details updated successfully.")
        
        # تحديث نافذة البحث بعد حفظ التغييرات
        update_search_results(book_id, content)
    
    def delete_book():
        confirm = messagebox.askyesno("Delete Book", "Are you sure you want to delete this book?")
        if confirm:
            db = sqlite3.connect("books.db")
            cr = db.cursor()
            cr.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            db.commit()
            db.close()
            
            edit_window.destroy()
            messagebox.showinfo("Success", "Book deleted successfully.")
            
            # تحديث نافذة البحث بعد الحذف
            update_search_results(book_id, content)
    
    # أزرار الحفظ والحذف
    tk.Button(edit_window, text="Save Changes", bg="#6f42c1", fg="white", command=save_changes).pack(pady=10)
    tk.Button(edit_window, text="Delete Book", bg="red", fg="white", command=delete_book).pack(pady=10)
    tk.Button(edit_window, text="Close", bg="gray", fg="white", command=edit_window.destroy).pack(pady=10)

def update_search_results(book_id, content):
    # استرجاع الكتاب المحدث من قاعدة البيانات
    db = sqlite3.connect("books.db")
    cr = db.cursor()
    cr.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    row = cr.fetchone()
    db.close()
    
    # تحويل البيانات المسترجعة إلى قاموس
    result = {
        "id": row[0],
        "title": row[1],
        "author": row[2],
        "genre": row[3],
        "copies": row[4]
    }
    
    # تحديث واجهة البحث
    display_search_results([result], content)

    
    
def switch_to_search_student(content):
    # تنظيف المحتوى الحالي
    for widget in content.winfo_children():
        widget.destroy()

    # إضافة العنوان
                            # تحميل الصورة وتعيينها كخلفية
        try:
            bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
            bg_img = Image.open(bg_image_path)
            bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
            bg_photo = ImageTk.PhotoImage(bg_img)
       
            # وضع الصورة كخلفية
            bg_label = tk.Label(content, image=bg_photo)
            bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
        except Exception as e:
            print(f"Error loading background image: {e}")
    header_label = tk.Label(content, text="Search Student", font=("Arial", 18, "bold"), bg="#f8f9fa")
    header_label.pack(pady=10)

    # إطار النموذج
    form_frame = tk.Frame(content, bg="white", padx=30, pady=30, relief=tk.RIDGE, bd=2)
    form_frame.pack(pady=20)

    # إضافة Label فوق حقل الإدخال
    label_search = tk.Label(form_frame, text="Enter Student ID:", bg="white", font=("Arial", 16))
    label_search.grid(row=0, column=0, padx=20, pady=20)

    # حقل الإدخال
    entry_search_query = tk.Entry(form_frame,  font=("Arial", 16), width=40)
    entry_search_query.grid(row=1, column=0, padx=20, pady=20)

    # زر البحث
    search_button = tk.Button(content, text="Search", font=("Arial", 16), bg="#6A1B9A", fg="white",
                              command=lambda: search_student_by_id(entry_search_query.get(), content))
    search_button.pack( pady=20)

# دالة البحث عن طالب باستخدام ID
# دالة البحث عن الطلاب باستخدام ID
def search_student_by_id(student_id, content):
    if not student_id.strip():
        messagebox.showerror("Input Error", "The ID field cannot be empty.")
        return

    try:
        db = sqlite3.connect("students.db")
        cr = db.cursor()
        cr.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        results = cr.fetchall()

        if results:
            students = [
                {"id": row[0], "name": row[1], "branch": row[2], "contact": row[3]} 
                for row in results
            ]
            display_students_results(students, content)
        else:
            messagebox.showinfo("No Results", "No students found with the given ID.")

        db.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# دالة عرض جميع النتائج
def display_students_results(students, content):
    # مسح الشاشة الحالية
    for widget in content.winfo_children():
        widget.destroy()
                            # تحميل الصورة وتعيينها كخلفية
        try:
            bg_image_path =r"D:\PYthon projects\Final Project LMS\rb_20499 (1).png"  # ضع مسار الصورة هنا
            bg_img = Image.open(bg_image_path)
            bg_img = bg_img.resize((1500, 1000))  # تعديل الحجم حسب الحاجة
            bg_photo = ImageTk.PhotoImage(bg_img)
       
            # وضع الصورة كخلفية
            bg_label = tk.Label(content, image=bg_photo)
            bg_label.image = bg_photo  # الاحتفاظ بالمرجع للصورة
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # ملء النافذة بالكامل
        except Exception as e:
            print(f"Error loading background image: {e}")
    # عنوان النتائج
    header_label = tk.Label(content, text="Students Details", font=("Arial", 24, "bold"), bg="#f8f9fa")
    header_label.pack(pady=10)

    # إطار الجدول
    table_frame = tk.Frame(content, bg="white", padx=35, pady=35, relief=tk.RIDGE, bd=2)
    table_frame.pack(pady=25)

    # إعداد العناوين
    headers = ["ID", "Name", "Branch", "Contact"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 16, "bold"), bg="#f0f0f0", padx=15, pady=10, relief=tk.GROOVE).grid(row=0, column=col, sticky="nsew")

    # عرض بيانات الطلاب
    for row, student in enumerate(students, start=1):
        tk.Label(table_frame, text=student["id"], font=("Arial", 16), bg="white", padx=15, pady=10).grid(row=row, column=0, sticky="nsew")
        tk.Label(table_frame, text=student["name"],  font=("Arial", 16), bg="white", padx=15, pady=10).grid(row=row, column=1, sticky="nsew")
        tk.Label(table_frame, text=student["branch"],  font=("Arial", 16), bg="white", padx=15, pady=10).grid(row=row, column=2, sticky="nsew")
        tk.Label(table_frame, text=student["contact"],  font=("Arial", 16), bg="white", padx=15, pady=10).grid(row=row, column=3, sticky="nsew")

    # تحسين تخطيط الأعمدة
    for col in range(len(headers)):
        table_frame.grid_columnconfigure(col, weight=1)

    # Start the login window
    login_window.mainloop()
   #------------------------------------------------------------------------------------
def sign_in():
    email = email_entry.get()
    password = password_entry.get()

    # Check if email and password match the correct values
    correct_email = "user@admin.com"
    correct_password = "412300178"

    if email == correct_email and password == correct_password:
        messagebox.showinfo("Welcome", "Welcome to the Library Management System!")
        login_window.destroy()  # Close the login window
        open_library_system()  # Open the library management system
    else:
        messagebox.showerror("Login Failed", "Incorrect email or password. Please try again.")

# Create login window
# إنشاء النافذة الرئيسية
login_window = tk.Tk()
login_window.title("Login Page")
login_window.geometry("800x500")  # ضبط أبعاد النافذة
login_window.configure(bg="#E5E5E5")

# حساب موقع النافذة لجعلها في منتصف الشاشة
window_width = 800
window_height = 500

# الحصول على أبعاد الشاشة
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

# حساب الإحداثيات للتمركز
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# ضبط موضع النافذة
login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
login_window.resizable(False, False)  # منع تغيير الحجم
login_window.attributes('-toolwindow', 1)  # تحويل النافذة إلى نافذة أدوات

# Left frame for sign-in
sign_in_frame = tk.Frame(login_window, bg="white", width=400, height=400)
sign_in_frame.pack(side="left", fill="both", expand=True)

# Right frame for hello friend
hello_frame = tk.Frame(login_window, bg="#6A1B9A", width=400, height=400)
hello_frame.pack(side="right", fill="both", expand=True)

# Sign-in widgets
tk.Label(sign_in_frame, text="Sign In", font=("Arial", 24), bg="white").pack(pady=20)
tk.Label(sign_in_frame, text="Email", font=("Arial", 12), bg="white").pack(pady=(10, 5))
email_entry = tk.Entry(sign_in_frame, font=("Arial", 12), width=30, bg="#F5F5F5")
email_entry.pack(pady=5)

tk.Label(sign_in_frame, text="Password", font=("Arial", 12), bg="white").pack(pady=(10, 5))
password_entry = tk.Entry(sign_in_frame, font=("Arial", 12), width=30, show="*", bg="#F5F5F5")
password_entry.pack(pady=5)

tk.Button(sign_in_frame, text="SIGN IN", font=("Arial", 12), bg="#6A1B9A", fg="white", width=15, command=sign_in).pack(
    pady=20)

# Hello friend widgets
tk.Label(hello_frame, text="Hello, Friend!", font=("Arial", 24), bg="#6A1B9A", fg="white").pack(pady=20)
tk.Label(hello_frame, text="Welcome to the Library System", font=("Arial", 12), bg="#6A1B9A", fg="white").pack(pady=5)
# إضافة الصورة داخل frame
image_frame = tk.Frame(hello_frame, bg="#6A1B9A")
image_frame.pack(pady=20)

# تحميل الصورة باستخدام PIL
image_path = r"D:\PYthon projects\Final Project LMS\rb_7875 (1).png"  # ضع مسار الصورة هنا
image = Image.open(image_path)
image = image.resize((250, 250), Image.Resampling.LANCZOS)  # تغيير حجم الصورة
photo = ImageTk.PhotoImage(image)

# عرض الصورة
image_label = tk.Label(image_frame, image=photo, bg="#6A1B9A")
image_label.pack()
create_database()
login_window.mainloop()