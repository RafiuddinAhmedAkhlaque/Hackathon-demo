# Greeting API

A simple Flask API that provides greeting endpoints.

## Endpoints

### GET /hello
Returns a generic greeting.

**Response:**
```json
{
  "message": "Hello, World!"
}
```

### GET /hello/<name>
Returns a personalized greeting for the given name.

**Parameters:**
- `name` (string): The name to greet. Must not be empty or contain numbers.

**Success Response (200):**
```json
{
  "message": "Hello, <name>!"
}
```

**Error Response (400):**
```json
{
  "error": "Name cannot be empty",
  "message": "Please provide a valid name"
}
```

Or:
```json
{
  "error": "Name cannot contain numbers", 
  "message": "Please provide a name without numbers"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "greeting-api"
}
```

## Running the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The API will be available at `http://localhost:8000`.

## Running Tests

```bash
# Run all tests
python -m pytest test_app.py

# Run with verbose output
python -m pytest test_app.py -v
```

## Examples

```bash
# Generic greeting
curl http://localhost:8000/hello

# Personalized greeting
curl http://localhost:8000/hello/Alice

# Error case - name with numbers
curl http://localhost:8000/hello/Alice123

# Health check
curl http://localhost:8000/health
```