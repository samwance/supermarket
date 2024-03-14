# Product marketplace

### Description: 
An online supermarket where you can find a lot of products with different categories and subcategories. Also you can add them in your cart. This project utilizes Django and PostgreSQL as the backend framework and database, respectively. User authorization is based on obtaining the token.
## Getting Started:

1) Clone the repository:
```
git clone https://github.com/samwance/supermarket.git
```
2) Navigate to the project directory:
```
cd supermarket
```
3) Create a .env file with the required environment variables. You can find a sample .env file in the project directory.

4) Run the Django migrations to set up the database:
```
python manage.py migrate
```
To load the database information:
```
python manage.py loaddata db_data.json=
```
To create a superuser for the Django admin site:
```
python manage.py createsuperuser
```

Start the Django development server:
```
python manage.py runserver
```
Open your web browser and navigate to http://localhost:8000/admin/ to access the Django admin site.

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
