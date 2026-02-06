# My Notes App

A simple, clean note-taking web application built with vanilla HTML, CSS, and JavaScript, with a Flask API backend.

## Features

- **Create Notes**: Add notes with a title and body content
- **View Notes**: See all your notes displayed in a responsive grid layout
- **Delete Notes**: Remove notes you no longer need
- **Persistent Storage**: Notes are saved in localStorage and persist across page refreshes
- **Modern UI**: Clean design with smooth animations and transitions
- **Responsive**: Works great on desktop, tablet, and mobile devices
- **API Backend**: Flask backend with hello and math endpoints
- **Request Logging**: Automatic logging of all HTTP requests with timing information

## API Endpoints

### GET /hello
Returns a simple greeting message.

**Response:**
```json
{
  "message": "Hello, World!"
}
```

**Status Code:** 200

### GET /goodbye
Returns a simple farewell message.

**Response:**
```json
{
  "message": "Goodbye, World!"
}
```

**Status Code:** 200

### POST /math
Performs basic arithmetic operations on two numbers.

**Request Body:**
```json
{
  "operation": "add",
  "a": 10,
  "b": 5
}
```

**Supported Operations:**
- `add` - Returns a + b
- `subtract` - Returns a - b
- `multiply` - Returns a * b
- `divide` - Returns a / b

**Response:**
```json
{
  "operation": "add",
  "a": 10,
  "b": 5,
  "result": 15
}
```

**Status Code:** 200

**Error Responses:**
- 400 - If operation is not supported
- 400 - If required fields (operation, a, b) are missing
- 400 - If dividing by zero (returns `{"error": "Cannot divide by zero"}`)
- 400 - If a or b are not valid numbers

**Example Usage:**
```bash
# Addition
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'

# Division
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 20, "b": 4}'

# With decimals
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "a": 3.5, "b": 2.2}'
```

## Request Logging

The Flask application includes comprehensive request logging middleware that automatically logs:
- Request method (GET, POST, etc.)
- Request path
- Response status code
- Request duration in milliseconds

All requests are logged at the INFO level using Python's logging module. Example log output:
```
2024-01-15 10:30:45,123 - app - INFO - Request: GET /hello - Status: 200 - Duration: 15.23 ms
2024-01-15 10:30:46,456 - app - INFO - Request: POST /math - Status: 200 - Duration: 12.78 ms
2024-01-15 10:30:47,789 - app - INFO - Request: GET /nonexistent - Status: 404 - Duration: 8.45 ms
```

## Getting Started

### Backend API
To run the Flask backend:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

The API will be available at `http://localhost:5000`

### Testing the Logging Middleware
You can test the logging functionality using the included demo script:

```bash
# Make sure the Flask server is running first (python app.py)
# Then in another terminal:
python demo_logging.py
```

This will make sample requests to the API endpoints and you can observe the log output in the Flask server console.

### Running Tests
To run the unit tests:

```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Run all tests
pytest -v

# Run specific test files
pytest test_hello.py -v
pytest test_math.py -v
pytest test_logging_middleware.py -v
```

## Project Structure

```
├── index.html                # Main HTML entry point
├── styles.css               # All CSS styles
├── app.js                   # JavaScript application logic (frontend)
├── app.py                   # Flask backend application with logging middleware
├── test_hello.py            # Unit tests for hello/goodbye endpoints
├── test_math.py             # Unit tests for math endpoint
├── test_logging_middleware.py # Unit tests for logging middleware
├── demo_logging.py          # Demo script to test logging functionality
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## Usage

### Frontend
1. **Create a note**: Enter a title and content in the form fields, then click "Save Note"
2. **View notes**: All saved notes appear as cards in the grid below the form
3. **Delete a note**: Click the × button on any note card to remove it
4. **Keyboard shortcut**: Press `Ctrl/Cmd + Enter` while in the form to quickly save a note

### API Usage
Test the API endpoints using curl or any HTTP client:

```bash
# Test the hello endpoint
curl http://localhost:5000/hello

# Test the goodbye endpoint
curl http://localhost:5000/goodbye

# Test the math endpoint
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'

# Test a non-existent endpoint (will return 404)
curl http://localhost:5000/nonexistent
```

All requests will be automatically logged with timing information.

## Browser Support

Works in all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## Technical Details

- **Frontend Storage**: Uses browser's localStorage API for data persistence
- **Frontend Dependencies**: Pure vanilla JavaScript with no external libraries
- **Backend**: Flask Python web framework
- **Testing**: pytest for unit tests with pytest-flask for Flask-specific testing
- **Logging**: Python's built-in logging module with INFO level
- **Request Timing**: High-precision timing using `time.time()` for millisecond accuracy
- **Math Operations**: Supports integer and decimal (float) numbers
- **Responsive design**: CSS Grid and Flexbox for layout
- **Animations**: CSS animations and transitions for smooth UX

## License

MIT License - Feel free to use and modify as needed.