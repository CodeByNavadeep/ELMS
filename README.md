
#  Employee Leave Management System (ELMS) – Flask Application

This is a role-based web application built using Flask to streamline and manage employee leave requests. 
The system supports three types of users: Admin, Manager, and Employee. 
Each role has its own set of features for submitting, reviewing, and managing leave applications.

----------

##  Features

-  **User Authentication** with role-based access
-  **Admin Panel**: Manage users, roles, and view leave reports
-  **Leave Management**: Apply, approve, reject, and track leave requests
-  **Dashboard Overview** per role
-  **Export Reports** as CSV and PDF
-  **SQLite/PostgreSQL Integration**
-  **Flask Templates (Jinja2)** for dynamic frontend rendering

----------

## 🔧 Tech Stack

| Layer           | Technology                   |
|-------------|----------------------------------|
| Backend         | Flask (Python)               |
| Frontend        | HTML, CSS, Bootstrap, Jinja2 |
| Database        | SQLite (or PostgreSQL ready) |
| Auth            | Flask-Login                  |
| Exporting       | `csv`, `reportlab` (PDF)     |
| Deployment      | Flask (dev server)           |
| Version Control | Git + GitHub                 |

----------

## 📂 Folder Structure

```
ELMS-Flask-App/
│
├── static/             # CSS, JS, images
├── templates/          # Jinja2 HTML templates
├── app.py              # Main application
├── models.py           # DB models and schema
├── forms.py            # WTForms (if used)
├── requirements.txt    # Python dependencies
├── README.md           # Project overview
└── instance/           # (optional) Config/db
```

----------

## ⚙️ Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/CodeByNavadeep/ELMS
cd ELMS
```

### 2. Create a Virtual Environment (optional)
```
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install Requirements
```
pip install -r requirements.txt
```

### 4. Set Environment Variables(Optional)
```
export FLASK_APP=app.py
export FLASK_ENV=development
```
(Use `set` on Windows)

### 5. Run the Application
```
flask run
```
Visit: [http://localhost:5000](http://localhost:5000)

---

## 🔑 Demo Login Credentials

| Role     | Username             | Password    |
|----------|----------------------|-------------|
| Admin    | Krishna              | 1234        |
| Manager  | Srinivas             | 1234        |
| Employee | Navadeep             | 1234        |

----------

## 📌 Future Improvements (Optional)

- Email notifications for leave status
- Unit and integration tests
- REST API support
- Docker support for containerization
- Mobile responsive UI

----------

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

----------

## 📜 License

This project is for internship learning and demonstration purposes.
