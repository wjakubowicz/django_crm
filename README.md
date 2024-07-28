# Django CRM Project

This Django CRM project is a simple yet powerful Customer Relationship Management system designed to help businesses manage their customer records efficiently.
Built with Django, it leverages the power of Python's web framework to provide a robust backend, coupled with a clean and responsive frontend.

## Key Features
- **Secure User Management**: Ensures authorized access with login, registration, and password handling.
- **2FA Login**: Implements two-factor authentication for enhanced security.
- **Centralized Dashboard**: Provides a unified view of all customer data.
- **Customer Records Management**: Add, update, view, and delete customer records.
- **Responsive Design**: Built with Bootstrap, ensuring a seamless experience across all devices.
- **Multiple UI Themes**: Ability to select and switch between different UI themes.
- **Interactive Maps**: View customer locations on an interactive map with options for tile style and marker clustering.
- **Data Import and Export**: Easily import and export customer data from and to popular formats for seamless integration with other systems.
- **PDF Printing**: Generate and print PDF documents directly.
- **Event Logging**: Logs user activities including record creation, updates, deletions, data imports and exports, and user authentication with timestamps, action types, and before-and-after states.
- **Address suggestions**: Enhances user input with address suggestions using Nominatim.

## Technologies
- **Backend**: Django
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Database**: SQLite (configurable to PostgreSQL, MySQL, etc.)

## Future Enhancements
- Define user roles and permissions
- Ensure data encryption
- Implement automatic database backup
- Improve language support and enable language switching
- Format the phone number to the international format
- Implement the option to export the map to PDF

## Installation
To get this project up and running on your local machine, follow these steps:

1. **Clone the Repository**
```bash
   git clone https://github.com/wjakubowicz/django_crm.git
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
  source virt/bin/activate
```

3. **Install Dependencies**
```bash
   pip install -r requirements.txt
```

4. **Migrate Database**
```bash
cd crm
python manage.py migrate
```
5. **Run the Server**
```bash
cd crm
python manage.py runserver
```

## Used libraries
- [Folium](https://github.com/python-visualization/folium)
- [Geopy](https://github.com/geopy/geopy)
- [jQuery](https://github.com/jquery/jquery)
- [DataTables](https://github.com/DataTables/DataTablesSrc)
- [Feather Icons](https://github.com/feathericons/feather)
- [django-import-export](https://github.com/django-import-export/django-import-export)
- [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- [crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5)
- [django-phonenumber-field](https://github.com/stefanfoulis/django-phonenumber-field)
- [django-two-factor-auth](https://github.com/jazzband/django-two-factor-auth)