E-Commerce Application

An e-commerce web application built using Django for the backend and React for the frontend. This project allows users to browse products, add items to their cart, and place orders. It also includes features for sellers to manage their inventory and for customers to view their order history.
Project Structure

E-Commerce/
│
├── customer_app/          # Manages customer data and operations
├── product_app/           # Handles product information and management
├── project/               # Main Django project settings and URLs
├── seller_app/            # Manages seller operations and inventory
├── manage.py              # Django project management file
├── requirements.txt       # Python dependencies
└── frontend/              # Contains React frontend files

Features
Customer

    User authentication and profile management
    View products and add them to the cart
    Place orders and view order history

Seller

    Seller authentication and profile management
    Add and manage product listings
    View inventory and sales analytics

Admin

    Manage users, products, and orders
    View detailed sales reports and analytics

Technologies Used

    Backend: Django, Django REST Framework
    Frontend: React, Axios for API requests
    Database: SQLite
    Others: JWT for authentication, Material UI for styling

Prerequisites

    Python: 3.7+
    Node.js: 12.0+
    Django: 3.2+
    React: 17.0+

Getting Started
1. Clone the Repository

git clone https://github.com/yamini-31/E-Commerce.git
cd E-Commerce

2. Backend Setup

    Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

Install backend dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser (for accessing the Django admin):

python manage.py createsuperuser

Run the backend server:

    python manage.py runserver

    The backend will be running at http://127.0.0.1:8000.

3. Frontend Setup

    Navigate to the frontend directory:

cd frontend

Install frontend dependencies:

npm install

Start the frontend development server:

    npm start

    The frontend will be running at http://localhost:3000.

4. Environment Variables

Create a .env file in the root of the project to store environment variables. Example:

# Django settings
SECRET_KEY=your_secret_key
DEBUG=True

# React settings
REACT_APP_API_URL=http://127.0.0.1:8000/api

API Documentation

The backend API is documented using Django REST Framework's built-in browsable API. You can access it by navigating to http://127.0.0.1:8000/api/ in your browser when the backend server is running.
Usage

    Customer: Users can sign up, log in, browse products, add items to the cart, and place orders.
    Seller: Sellers can log in, add new products, and manage inventory.
    Admin: Admin users can access Django's admin panel to manage all data.

Contributing

If you'd like to contribute to this project, please fork the repository and make a pull request. Contributions, whether bug reports, feature requests, or improvements, are welcome.
License

This project is licensed under the MIT License.
