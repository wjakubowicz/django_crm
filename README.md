# Django CRM Project

This Django CRM project is a simple yet powerful Customer Relationship Management system designed to help businesses manage their customer records efficiently.
Built with Django, it leverages the power of Python's web framework to provide a robust backend, coupled with a clean and responsive frontend.

## Key Features
- **Secure User Management**: Ensures authorized access with login, registration, and password handling.
- **Centralized Dashboard**: Provides a unified view of all customer data.
- **Customer Records Management**: Add, update, view, and delete customer records.
- **Responsive Design**: Built with Bootstrap, ensuring a seamless experience across all devices.
- **Multiple UI Themes**: Ability to select and switch between different UI themes.
- **Interactive Maps**: View customer locations on an interactive map with options for tile style and marker clustering.

## Technologies
- **Backend**: Django
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Database**: SQLite (configurable to PostgreSQL, MySQL, etc.)

## Future Enhancements
- Define user roles and permissions
- Enable 2FA login using an authenticator app or a hardware token
- Ensure data encryption
- Export data to other document formats such as PDF and XLSX  
- Implement automatic database backup
- Improve language support and enable language switching
- Log changes made to the database

## Installation
To get this project up and running on your local machine, follow these steps:

1. **Clone the Repository**
```bash
   git clone https://github.com/wjakubowicz/django_crm.git
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

## Used libraries
- [Folium](https://github.com/python-visualization/folium)
- [Geopy](https://github.com/geopy/geopy)
- [jQuery](https://github.com/jquery/jquery)
- [DataTables](https://github.com/DataTables/DataTablesSrc)
- [Feather Icons](https://github.com/feathericons/feather)