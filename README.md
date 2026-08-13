# Online Shopping Application API

<p align="center">
  A secure and scalable backend API for managing an online shopping application.
</p>

<p align="center">
  Built with FastAPI, SQLAlchemy, Pydantic, and role-based access control.
</p>

---

## Project Overview

The **Online Shopping Application API** is a backend project developed using **FastAPI** and **SQLAlchemy**.

The application supports the complete online shopping journey, including user registration, authentication, product browsing, cart management, checkout, and order tracking.

In Week 3, the project was enhanced with administrative capabilities, authentication dependencies, role-based access control, product and category management, user-role management, and Swagger/OpenAPI documentation.

---

## Key Features

### Customer Features

- User registration
- User login and authentication
- View user information
- View product categories
- View and search products
- Add products to the shopping cart
- Update cart item quantities
- Remove products from the cart
- Checkout and place orders
- View order history
- View order details
- Request validation using Pydantic schemas

### Administrative Features

- Create new products
- Update existing products
- Deactivate products
- Create new categories
- Update existing categories
- View all customer orders
- Update user roles
- Protect administrative APIs using role-based authorization
- Allow support and operations users to view orders
- Validate duplicate products and categories
- Handle database transaction failures safely

### API Documentation

- Interactive Swagger UI
- OpenAPI documentation
- Request body validation
- Path parameter validation
- Authentication support through the Swagger `Authorize` button
- Organized endpoint sections using router tags

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Programming language |
| FastAPI | Backend web framework |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Request and response validation |
| SQLite/PostgreSQL | Database options |
| Uvicorn | ASGI application server |
| Swagger UI | Interactive API testing |
| OpenAPI | API specification and documentation |

---

## Project Architecture

The project follows a layered backend architecture:

```text
Client or Swagger UI
        |
        v
Routers
        |
        v
Services
        |
        v
Repositories
        |
        v
SQLAlchemy Models
        |
        v
Database
```

### Layer Responsibilities

| Layer | Responsibility |
|---|---|
| Routers | Define API endpoints and receive HTTP requests |
| Schemas | Validate request bodies and response data |
| Services | Implement business rules and application logic |
| Repositories | Perform database queries and persistence operations |
| Models | Represent database tables using SQLAlchemy |
| Database | Manage connections, sessions, and transactions |
| Utilities | Provide authentication dependencies and helper functions |

---

## Project Structure

```text
WEEK3-KHUSHI_LNU/
|
|-- env/
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
|   |   |-- admin_schema.py
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
|   |   |-- __init__.py
|   |   |-- user_router.py
|   |   |-- category_router.py
|   |   |-- product_router.py
|   |   |-- cart_router.py
|   |   |-- order_router.py
|   |   |-- admin_router.py
|   |
|   |--tests/
|   |   |-- conftest.py
|   |   |-- test_product.py
|   |   |-- test_user.py
|   |
|   |-- utils/
|   |   |-- auth_dependencies.py
|   |   |-- security.py
|
|-- requirements.txt
|-- .env
|-- pytes.ini
|-- .gitignore
|-- README.md
```

---

## API Endpoints

The final URL depends on the router prefixes configured in `main.py`.

The customer endpoints below use the `/api` prefix. The admin router uses the `/admin` prefix. If `main.py` registers the admin router with an additional `/api` prefix, the final paths will appear as `/api/admin/...`.

### User APIs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/users/register` | Register a new user |
| `POST` | `/api/users/login` | Log in and receive authentication details |
| `GET` | `/api/users/{user_id}` | Retrieve user information |

### Category APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/categories` | View available categories |

### Product APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/products` | View active products |
| `GET` | `/api/products/{product_id}` | View product details |
| `GET` | `/api/products/search` | Search for products |

### Cart APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/cart/{user_id}` | View a user's cart |
| `POST` | `/api/cart/add` | Add a product to the cart |
| `PUT` | `/api/cart/update/{cart_item_id}` | Update cart quantity |
| `DELETE` | `/api/cart/remove/{cart_item_id}` | Remove a cart item |

### Order APIs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/orders/checkout` | Place an order |
| `GET` | `/api/orders/{user_id}` | View order history |
| `GET` | `/api/orders/details/{order_id}` | View order details |

---

## Administrative APIs

Administrative routes are defined in `admin_router.py`.

The router uses:

- Prefix: `/admin`
- Swagger tag: `Admin`

These endpoints appear under the **Admin** section in Swagger UI.

### Product Management

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/admin/products` | Admin | Create a product |
| `PUT` | `/admin/products/{product_id}` | Admin | Update a product |
| `DELETE` | `/admin/products/{product_id}` | Admin | Deactivate or delete a product |

When the `Product` model contains an `IsActive` field, deleting a product performs a soft delete by setting `IsActive` to `False`.

### Category Management

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/admin/categories` | Admin | Create a category |
| `PUT` | `/admin/categories/{category_id}` | Admin | Update a category |

### Order Management

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/admin/orders` | Admin, Support, Operations | View all orders |

Orders are returned with the newest orders first based on the order date.

### User Role Management

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `PATCH` | `/admin/users/{user_id}/role` | Admin | Update a user's role |

Only an authenticated administrator can update another user's role.

---

## Role-Based Access Control

The application verifies the authenticated user's role before allowing access to protected endpoints.

| Role | Permissions |
|---|---|
| `admin` | Manage products, manage categories, view all orders, update user roles |
| `support` | View all orders |
| `operations` | View all orders |
| `customer` | Browse products, manage cart, place orders, view personal orders |

### Authorization Dependencies

- `get_current_user` identifies the authenticated user.
- `require_admin` allows only users with the `admin` role.
- `require_order_staff` allows users with the `admin`, `support`, or `operations` role.

Unauthorized users receive an appropriate HTTP error response.

---

## Authentication Flow

The request flow for a protected endpoint is:

1. A user registers or logs in.
2. The application authenticates the user.
3. The user sends an authentication token with the request.
4. `get_current_user` identifies the user.
5. The application checks the user's role.
6. FastAPI validates the request body and path parameters.
7. The router executes the requested operation.
8. The service or repository accesses the database.
9. The transaction is committed.
10. The API returns a JSON response.

```text
Client or Swagger UI
        |
        v
Authentication Token
        |
        v
get_current_user
        |
        v
Role Validation
        |
        v
Router Endpoint
        |
        v
Service or Repository
        |
        v
Database
        |
        v
JSON Response
```

---

## Database Transaction Handling

Database write operations follow a safe transaction process:

1. Query the required record.
2. Validate the requested operation.
3. Create or update the SQLAlchemy model.
4. Add the object to the database session.
5. Commit the transaction.
6. Refresh the object.
7. Return the updated data.
8. Roll back the transaction if a database error occurs.

This prevents incomplete database changes when an operation fails.

---

## Validation and Error Handling

The API includes:

- Positive integer validation for resource IDs
- Duplicate product-name validation
- Duplicate category-name validation
- Category existence validation
- Product price conversion using `Decimal`
- Pydantic request-body validation
- Authentication and authorization checks
- Database rollback after failed transactions
- Meaningful HTTP status codes and error messages

### Common HTTP Responses

| Status Code | Meaning |
|---|---|
| `200 OK` | Request completed successfully |
| `201 Created` | Resource created successfully |
| `400 Bad Request` | Invalid request data |
| `401 Unauthorized` | Authentication is missing or invalid |
| `403 Forbidden` | User does not have the required role |
| `404 Not Found` | Requested resource does not exist |
| `409 Conflict` | Duplicate resource or conflicting operation |
| `500 Internal Server Error` | Database or server failure |

---

## Swagger UI

FastAPI automatically generates interactive API documentation.

After starting the application, open the `/docs` route in a browser.

Swagger UI displays the available API groups, including:

- User
- Category
- Product
- Cart
- Order
- Admin

### Testing an Admin Endpoint

1. Open Swagger UI.
2. Select **Authorize**.
3. Enter a valid authentication token.
4. Select **Authorize** and close the dialog.
5. Open the **Admin** section.
6. Select an endpoint.
7. Select **Try it out**.
8. Enter the required path parameters.
9. Enter the request body when required.
10. Select **Execute**.
11. Review the response status and response body.

If the router is registered with an `/api` prefix, verify the final path displayed in Swagger.

---

## Running the Application

Create and activate a virtual environment, install the dependencies from `requirements.txt`, and start the FastAPI application using Uvicorn.

The application entry point is:

`product.main:app`

Once the application starts, use the `/docs` route to explore and test the APIs.

---

## Development Notes

- Register `admin_router.py` in `main.py`.
- Confirm the final route prefixes in Swagger UI.
- Use a valid token when testing protected endpoints.
- Keep authentication secrets and database configuration in `.env`.
- Do not commit passwords, tokens, or secrets to source control.
- Ensure inactive products are excluded from customer-facing product listings.
- Use soft deletion where possible to preserve historical order relationships.
- Keep user roles consistent throughout the database, schemas, and authorization dependencies.
- Remove duplicate imports from `admin_router.py` for cleaner project maintenance.

---

## Project Summary

This project demonstrates how to build a structured shopping API with:

- Layered architecture
- RESTful endpoints
- Database persistence
- Authentication
- Role-based authorization
- Administrative workflows
- Input validation
- Transaction management
- Interactive Swagger documentation

It provides a strong foundation for extending the application with payment integration, inventory management, order-status tracking, automated testing, and production deployment.

---

<table align="center">
  <tr>
    <td align="center" width="420">
      <strong>Built with dedication by</strong>
      <br><br>
      <strong>KHUSHI</strong>
      <strong>K8@deloitte.com</strong>
      <br><br>
      <sub>Online Shopping Application API | Week 3</sub>
    </td>
  </tr>
</table>
