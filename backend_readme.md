
# Backend README - Django Application

## Overview

This backend is built using Django within a virtual environment. The application is located in the `Rest` folder. It uses two custom databases and one built-in database to manage user authentication, medication data, and order history.

### Databases Used

1. **Users (built-in)**  
   This is the built-in Django database used for user authentication. It handles the login and registration endpoints through Django's authentication middleware.

2. **Refill Orders**  
   This database stores the refill orders received from users. It contains the following columns:
   - `id`: Primary key, auto-incremented.
   - `user_id`: Foreign key pointing to the user who placed the order.
   - `orderlist`: List of products in the order and their respective quantities.
   - `totalprice`: A double variable storing the total price of the order.

3. **Medications**  
   This database holds the product list of medications available for users. Currently, it is populated with dummy data from a `list.json` file and a dummy endpoint. It includes the following columns:
   - `id`: Primary key.
   - `name`: Name of the medication.
   - `category`: The category to which the medication belongs.
   - `dosage_form`: Form in which the medication is administered (e.g., tablet, syrup).
   - `brand_name`: Brand name of the medication.
   - `concentration`: Concentration of the active ingredient.
   - `price`: Price of the medication.
   - `refill_requests`: Number of refill requests made for this medication.
   - `refills_issued`: Number of refills fulfilled for this medication.
   - `image_url`: URL to the image of the medication.

### Admin Database

An admin-specific dummy database is also provided for future enhancements to offer exclusive functionalities for admins.

## API Endpoints

Below are the various API endpoints exposed by the backend:

### 1. **Chart Data Endpoint**  
**URL:** `medications/chart`  
**Method:** `GET`  
**View:** `GetAnalytics`  
This endpoint returns analytical data based on the `USERS`, `Medications`, and `Refill Orders` databases to generate charts for the dashboard.

### 2. **Place Order Endpoint**  
**URL:** `medications/order`  
**Method:** `POST`  
**View:** `IssueOrderView`  
This endpoint registers a user’s order in the `Refill Orders` database. It processes the order and stores it for further action.

### 3. **Fetch Medications Endpoint**  
**URL:** `medications/fetch`  
**Method:** `GET`  
**View:** `LoadMedicationsView`  
This endpoint retrieves the list of medications from the `Medications` database and returns them to the user.

### 4. **Insert Dummy Data Endpoint**  
**URL:** `data/insert`  
**Method:** `POST`  
**View:** `populate`  
A dummy endpoint for testing purposes. It allows for the insertion of data into the database.

### 5. **Refresh Token Endpoint**  
**URL:** `token/refresh`  
**Method:** `POST`  
**View:** `RefreshAccessTokenView`  
This endpoint accepts a refresh token and responds with a new valid access token.

### 6. **User Registration Endpoint**  
**URL:** `register`  
**Method:** `POST`  
**View:** `RegisterView`  
This endpoint accepts user registration data and inserts it into the `Users` database.

### 7. **User Login Endpoint**  
**URL:** `login`  
**Method:** `POST`  
**View:** `LoginView`  
This endpoint validates the user’s credentials against the `Users` database using Django’s middleware. If successful, it responds with a JWT token.

---

## View Explanation

Each view in the application is detailed in the `views.py` file, providing a clear explanation of what each one does and how it operates.

## Setup Instructions

1. **Install Dependencies**  
   To get started with the backend, ensure you have set up a virtual environment and install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Migrations**  
   Run the migrations to set up the databases:
   ```bash
   python manage.py migrate
   ```

3. **Start the Development Server**  
   To run the server locally, use:
   ```bash
   python manage.py runserver
   ```
   to populate database with dummy data
   ```bash
   python populate.py
   ```
