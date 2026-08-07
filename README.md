<!-- # Online Shopping Application API

This is a beginner-friendly backend API for an online shopping application.  
The project is built using FastAPI and SQLAlchemy.

## Features

- User registration and login
- View and search products
- View product categories
- Add, update, and remove cart items
- Checkout and place orders
- View order details
- Basic validations 

## Technologies Used

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite/PostgreSQL
- Uvicorn

## Project Structure
KHUSHILNU/
    |
    |-- product/
    |   |
    |   |-- __init__.py
    |   |-- main.py
    |   |
    |   |-- db/
    |   |   |-- __init__.py
    |   |   |-- base.py
    |   |   |-- session.py
    |   |
    |   |-- models/
    |   |   |-- __init__.py
    |   |   |-- user.py
    |   |   |-- category.py
    |   |   |-- product.py
    |   |   |-- cart.py
    |   |   |-- order.py
    |   |   |-- order_detail.py
    |   |
    |   |-- schemas/
    |   |   |-- __init__.py
    |   |   |-- user_schema.py
    |   |   |-- category_schema.py
    |   |   |-- product_schema.py
    |   |   |-- cart_schema.py
    |   |   |-- order_schema.py
    |   |
    |   |-- repositories/
    |   |   |-- __init__.py
    |   |   |-- user_repository.py
    |   |   |-- category_repository.py
    |   |   |-- product_repository.py
    |   |   |-- cart_repository.py
    |   |   |-- order_repository.py
    |   |   |-- order_detail_repository.py
    |   |
    |   |-- services/
    |   |   |-- __init__.py
    |   |   |-- user_service.py
    |   |   |-- category_service.py
    |   |   |-- product_service.py
    |   |   |-- cart_service.py
    |   |   |-- order_service.py
    |   |
    |   |-- routers/
    |       |-- __init__.py
    |       |-- user_router.py
    |       |-- category_router.py
    |       |-- product_router.py
    |       |-- cart_router.py
    |       |-- order_router.py
    |
    |-- tests/
    |
    |-- requirements.txt
    |-- .env
    |-- .gitignore
    |-- README.md -->


<!-- ### Folder Description

- `db/` — Database connection
- `models/` — Database tables
- `schemas/` — Request and response validation
- `repositories/` — Database operations
- `services/` — Business logic
- `routers/` — API endpoints
- `utils/` — Helper functions and exceptions

## API Endpoints

### User APIs
- `POST /api/users/register` — Register a new user
- `POST /api/users/login` — Login
- `GET /api/users/{user_id}` - Retrieve a user info

### Category APIs

- `GET /api/categories` — View all categories
- `POST /api/categories` — View all categories

### Product APIs

- `GET /api/products` — View all products
- `POST /api/products` — create a product
- `GET /api/products/{id}` — View product details
- `GET /api/products/search` — Search products


### Cart APIs

- `GET /api/cart/{user_id}` — View cart
- `POST /api/cart/add` — Add product to cart
- `PUT /api/cart/update/{cart_item_id}` — Update cart quantity
- `DELETE /api/cart/remove/{cart_item_id}` — Remove cart item

### Order APIs

- `POST /api/orders/checkout` — Place an order
- `GET /api/orders/{user_id}` — View order history
- `GET /api/orders/details/{order_id}` — View order details

### Default APIs

- `/` — Root
