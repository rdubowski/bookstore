# Yourbook
Live  can be viewed at https://your-book.herokuapp.com/

Yourbook is a bookstore website made using Django Rest Framework and React.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is simple bookstore website. Features:
* Register and Login
  * JWT Authentication to connect DRF and React
  * Can login with username or email
* Books
  * View Books
  * As admin user: add, edit, delete books
* Orders:
  * Make orders
  * Pay for order with PayPal
  * As admin user: marking order as delivered, delete order, edit order
* Reviews:
  * Add Review to bought books
  * Books with best reviews displayed at top of homescreen
	
## Technologies
Project is created with:
* Django(Django Rest Framework)
* Pytest
* React(Redux, React Router)
* Bootstrap

## Setup
To run this project:
1. Clone project
``` git clone https://github.com/rdubowski/bookstore/ ```
2. Create virtual environment: 
``` 
$ virtualenv myenv
$ myenv\scripts\activate
```
3. Install backend dependencies.
``` 
$ pip install -r requirements.txt
```
4. Install frontend dependencies.
```
$ cd frontend/
$ npm install
$ cd ..
```
5. Run server.
```
python manage.py runserver
```
