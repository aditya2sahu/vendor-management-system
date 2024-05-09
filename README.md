# Vendor Management System

Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance

## Installation

1. **Create a virtual environment and activate it:**

   For Linux/Mac:
   ```bash
   virtualenv myenv
   source myenv/bin/activate
   ```
   For Window:
   ```bash
   virtualenv myenv
   myenv/Scripts/activate
   ```
2. Clone the repository:

    ```bash
    https://github.com/aditya2sahu/vendor-management-system.git
    ```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Usage
1. Start the development server:
```bash
python manage.py runserver
```
3. Create a superuser:
```bash
python manage.py createsuperuser
```
5. Open your web browser and go to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access the admin panel.

## Endpoints

- **Sign Up:** [http://127.0.0.1:8000/auth/sing_up](http://127.0.0.1:8000/auth/sing_up)  
  Use this endpoint to sign up for a new account.

- **Login:** [http://127.0.0.1:8000/auth/login](http://127.0.0.1:8000/auth/login)  
  Use this endpoint to obtain JWT tokens. Send a POST request with email and password.

- **Vendor Profile Management:**
- Create a model to store vendor information including name, contact details, address, and a unique vendor code.
     [http://127.0.0.1:8000/api/vendors](http://127.0.0.1:8000/api/vendors): Create a new vendor.
     [http://127.0.0.1:8000/api/vendors/](http://127.0.0.1:8000/api/vendors/): List all vendors.
     [http://127.0.0.1:8000/api/vendor/id](http://127.0.0.1:8000/api/vendor/): Retrieve a specific vendor's details.
     [http://127.0.0.1:8000/api/vendor/update/id](http://127.0.0.1:8000/api/vendor/update/): Update a vendor's details.
     [http://127.0.0.1:8000/api/vendor/delete/id](http://127.0.0.1:8000/api/vendor/delete/): Delete a vendor.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
