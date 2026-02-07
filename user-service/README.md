# User Service

A FastAPI-based microservice that handles user registration, authentication, profile management, and address book functionality.

## Overview

The User Service is part of a larger microservices architecture and provides the following core functionalities:

- **User Registration**: Create new user accounts with validation
- **Authentication**: Login with JWT token-based authentication  
- **Profile Management**: Update user profile information
- **Address Book**: Manage user addresses for shipping and billing
- **Account Management**: User verification and account status management

## Features

- ✅ User registration with email and username validation
- ✅ Secure password hashing using bcrypt
- ✅ JWT token-based authentication
- ✅ User profile CRUD operations
- ✅ Address management (multiple addresses per user)
- ✅ Input validation using Pydantic models
- ✅ Comprehensive test coverage
- ✅ Health check endpoint

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Data Validation**: Pydantic 2.5.2
- **Authentication**: python-jose 3.3.0
- **Password Hashing**: passlib 1.7.4 with bcrypt 4.1.2
- **Testing**: pytest 7.4.3 with httpx 0.25.2

## Project Structure

```
user-service/
├── models/                 # Pydantic models for data validation
│   ├── user.py            # User-related models
│   ├── address.py         # Address models
│   └── session.py         # Authentication models
├── repositories/          # Data access layer
│   ├── user_repository.py # User data operations
│   └── address_repository.py # Address data operations
├── routes/                # API route handlers
│   ├── auth_routes.py     # Authentication endpoints
│   ├── user_routes.py     # User management endpoints
│   └── address_routes.py  # Address management endpoints
├── services/              # Business logic layer
│   ├── auth_service.py    # Authentication business logic
│   ├── user_service.py    # User management business logic
│   └── address_service.py # Address management business logic
├── utils/                 # Utility functions
│   ├── password_hasher.py # Password hashing utilities
│   ├── token_manager.py   # JWT token management
│   └── validators.py      # Custom validators
├── tests/                 # Test suite
│   ├── test_*.py          # Unit tests
│   └── conftest.py        # Test configuration
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── pytest.ini           # pytest configuration
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login with email/password
- `POST /auth/logout` - User logout (token invalidation)
- `POST /auth/refresh` - Refresh access token

### User Management
- `POST /users/` - Register a new user
- `GET /users/{user_id}` - Get user profile
- `PUT /users/{user_id}` - Update user profile
- `DELETE /users/{user_id}` - Deactivate user account
- `GET /users/` - List users (with pagination)

### Address Management
- `POST /users/{user_id}/addresses/` - Add new address
- `GET /users/{user_id}/addresses/` - Get user addresses
- `PUT /users/{user_id}/addresses/{address_id}` - Update address
- `DELETE /users/{user_id}/addresses/{address_id}` - Delete address

### Health Check
- `GET /health` - Service health status

## Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd user-service
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

### Development Mode
```bash
python app.py
```

The service will start on `http://localhost:8001`

### Production Mode
```bash
uvicorn app:app --host 0.0.0.0 --port 8001
```

### Using Docker (if Dockerfile exists)
```bash
docker build -t user-service .
docker run -p 8001:8001 user-service
```

## Testing

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=. --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_user_service.py
```

## Configuration

The service uses environment variables for configuration:

- `JWT_SECRET_KEY` - Secret key for JWT token signing
- `JWT_ALGORITHM` - Algorithm for JWT token signing (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)

## API Documentation

Once the service is running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8001/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8001/redoc`
- **OpenAPI schema**: `http://localhost:8001/openapi.json`

## Data Models

### User Model
```python
{
    "id": "uuid",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Address Model
```python
{
    "id": "uuid",
    "user_id": "uuid",
    "type": "billing|shipping",
    "street": "123 Main St",
    "city": "Anytown",
    "state": "ST",
    "zip_code": "12345",
    "country": "US",
    "is_default": false
}
```

## Development

### Adding New Features

1. **Models**: Add/modify Pydantic models in `models/`
2. **Repository**: Implement data access logic in `repositories/`
3. **Service**: Add business logic in `services/`
4. **Routes**: Create API endpoints in `routes/`
5. **Tests**: Add comprehensive tests in `tests/`

### Code Style

The project follows Python best practices:
- Type hints for all function parameters and return values
- Pydantic models for data validation
- Dependency injection pattern
- Clear separation of concerns (routes → services → repositories)

## Contributing

1. Follow the existing code structure and patterns
2. Add unit tests for new functionality
3. Update this README if adding new features or endpoints
4. Ensure all tests pass before submitting changes

## Support

For questions or issues related to the User Service, please contact the development team or create an issue in the project repository.