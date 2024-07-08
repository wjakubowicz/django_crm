# Django CRM Project

This Django CRM project is a simple yet powerful Customer Relationship Management system designed to help businesses manage their customer records efficiently.
Built with Django, it leverages the power of Python's web framework to provide a robust backend, coupled with a clean and responsive frontend.

## Key Features
- **Secure User Management**: Ensures authorized access with login, registration, and password handling.
- **Centralized Dashboard**: Provides a unified view of all customer data.
- **Customer Records Management**: Add, update, view, and delete customer records.
- **Responsive Design**: Built with Bootstrap, ensuring a seamless experience across all devices.
- **Multiple UI Themes**: Ability to select and switch between different UI themes.

## Technologies
- **Backend**: Django
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Database**: SQLite (default), configurable to PostgreSQL, MySQL, etc.

## Future Enhancements:
- Display a checkmark next to the selected theme
- Better language support and language switching
- Gather coordinates based on the record's address
- Display the coordinates on a map with pins at each record address
- Export to popular document formats (PDF, CSV, XLSX, etc.)

## Installation
To get this project up and running on your local machine, follow these steps:

1. **Clone the Repository**
```bash
   git clone https://github.com/your-username/django-crm.git
   cd django-crm
```
2. **Set Up a Virtual Environment**

- For Windows:
```bash
  python -m venv virt
  .\venv\Scripts\activate
```

- For macOS and Linux:
```bash
  python3 -m venv virt
  source venv/bin/activate
```

3. **Install Dependencies**
```bash
   pip install -r requirements.txt
```

4. **Migrate Database**
```bash
python manage.py migrate
```

5. **Run the Server**
```bash
python manage.py runserver
```