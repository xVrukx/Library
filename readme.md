# 📚 Library Management System (Python + MySQL + Tkinter)

A simple yet powerful library management system built using Python, MySQL, and Tkinter GUI. Designed for schools, colleges, and personal book collections.

---

## 🧰 Features

- ✅ Add, edit, delete books
- ✅ Add, edit, delete members
- ✅ Issue and return books
- ✅ View all records (books & members)
- ✅ Status tracking (available/issued)
- ✅ GUI built with Tkinter
- ✅ MySQL backend integration
- ✅ Error handling and validation

---

## 💻 Tech Stack

| Technology | Purpose                |
|------------|------------------------|
| Python     | Core logic             |
| Tkinter    | GUI interface          |
| MySQL      | Database management    |
| `mysql-connector-python` | DB connectivity |

---

## ⚙️ Installation

1. **Install MySQL** and create a database:
   ```sql
   CREATE DATABASE library;
Clone the repo:

git clone https://github.com/vrukcodes/library-management-system
cd library-management-system
Install dependencies:

pip install mysql-connector-python
Update DB config in db_config.py:


DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "your_password"
DB_NAME = "library"
Run the App:

python app.py
🖥️ GUI Preview
![1750578974601](https://github.com/user-attachments/assets/f1aa3c1b-9e3f-4280-b212-99ffb0643dfe)


📂 Project Structure

📁 library-management-system/
│
├── app.py                  # Main app launcher
├── db_config.py           # MySQL connection details
├── database.sql           # Optional: DB schema (if available)
├── gui/
│   ├── add_book.py
│   ├── issue_book.py
│   └── ...
🚀 Future Features
 PDF export of book/member data

 Search & filter

 Fine calculation on late return

 Admin login

🙋‍♂️ Author
Vruk (vrukcodes)
Python + Backend Dev
GitHub: github.com/xVrukx

👩Guide
KI my sensei guided me and helped me throught this project

📄 License
MIT – Free to use, modify, and share.
