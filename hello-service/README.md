# Hello Service

A simple Flask API service that provides greeting endpoints.

## Endpoints

### GET /hello
Returns a generic greeting message.

**Response:**
```json
{
  "message": "Hello, World!"
}
```

### GET /hello/<name>
Returns a personalized greeting message for the specified name.

**Parameters:**
- `name` (string): The name to include in the greeting. Must not be empty or contain numbers.

**Success Response:**
```json
{
  "message": "Hello, <name>!"
}
```

**Error Response (400):**
```json
{
  "error": "Name cannot be empty"
}
```
or
```json
{
  "error": "Name cannot contain numbers"
}
```

### GET /health
Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "hello-service"
}
```

## Running the Service

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the service:
   ```bash
   python app.py
   ```

The service will start on `http://localhost:8006`.

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

## Examples

```bash
# Generic greeting
curl http://localhost:8006/hello

# Personalized greeting
curl http://localhost:8006/hello/Alice

# Error case - name with numbers
curl http://localhost:8006/hello/Alice123

# Health check
curl http://localhost:8006/health
```