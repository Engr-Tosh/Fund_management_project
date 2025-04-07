# Fund Management API

## Overview

This API provides a secure and efficient fund management system, allowing users to deposit, withdraw, and track their balance. It also includes an admin view for monitoring total deposits, withdrawals, and personal usage records.

## Features

- **User Authentication:** User registration, login, and profile management.
- **Fund Transactions:** Deposit and withdrawal functionalities.
- **Balance Management:** Real-time balance tracking for users.
- **Transaction Logging:** Comprehensive audit trail for all transactions.
- **Admin Overview:** Admin functionality to track total user funds and personal usage.

## Technologies Used

- **Django** (Backend Framework)
- **Django REST Framework (DRF)** (API Development)
- **MySQL** (Database)
- **Token-based Authentication** (User Authentication)

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Django 4.x
- Django REST Framework
- MySQL

### Clone the Repository

```bash
git clone https://github.com/Engr-Tosh/Fund_management_project/tiwiti-api.git
cd tiwiti-api
```

### Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### Run the Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| POST   | /api/tiwitifunds/register/ | User Registration |
| POST   | /api/tiwitifunds/login/    | User Login        |
| GET/PATCH    | /api/tiwiti/profile/  | User Profile      |

### Transactions

| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| POST   | /api/tiwitifunds/deposit/  | Make a Deposit        |
| POST   | /api/tiwitifunds/withdraw/ | Request a Withdrawal  |
| GET    | /api/tiwitifunds/balance/  | Retrieve User Balance |


## Project Structure

```
tiwiti-api/
|-- core/
|   |-- models.py  # User model
|   |-- serializers.py  # User authentication serializers
|   |-- views.py  # User authentication views
|   |-- urls.py  # Authentication routes
|
|-- transactions/
|   |-- models.py  # Deposit, Withdrawal, Balance models
|   |-- serializers.py  # Transaction serializers
|   |-- views.py  # Transaction views
    |-- test_transactions.py # API tests
|   |-- urls.py  # Transaction routes
|
|-- tiwiti_api/
|   |-- settings.py  # Project settings
|   |-- urls.py  # API route configuration
```

## Contributing

Feel free to fork this repository and contribute! Open an issue or submit a pull request with improvements.

## License

This project is licensed under the MIT License.

## Author

Amatotsero Divine Onome

