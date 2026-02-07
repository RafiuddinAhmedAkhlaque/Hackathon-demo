# My Notes App

A simple, clean note-taking web application built with vanilla HTML, CSS, and JavaScript, with Flask/Express API backends.

## Features

- **Create Notes**: Add notes with a title and body content
- **View Notes**: See all your notes displayed in a responsive grid layout
- **Delete Notes**: Remove notes you no longer need
- **Persistent Storage**: Notes are saved in localStorage and persist across page refreshes
- **Modern UI**: Clean design with smooth animations and transitions
- **Responsive**: Works great on desktop, tablet, and mobile devices
- **Dual API Backend**: Both Flask (Python) and Express (Node.js) backends available
- **Math Calculator API**: Perform basic arithmetic operations via API
- **Request Logging**: Automatic logging of all HTTP requests with timing information (Flask)

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

### GET /goodbye (Flask only)
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

**Supported operations:**
- `"add"` - Addition (a + b)
- `"subtract"` - Subtraction (a - b)
- `"multiply"` - Multiplication (a * b)
- `"divide"` - Division (a / b)

**Success Response:**
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

Missing fields:
```json
{
  "error": "Missing required field: operation"
}
```
**Status Code:** 400

Invalid operation:
```json
{
  "error": "Unsupported operation. Supported operations: add, subtract, multiply, divide"
}
```
**Status Code:** 400

Division by zero:
```json
{
  "error": "Cannot divide by zero"
}
```
**Status Code:** 400

Invalid numbers:
```json
{
  "error": "Fields 'a' and 'b' must be valid numbers"
}
```
**Status Code:** 400

## Request Logging (Flask Backend)

The Flask application includes comprehensive request logging middleware that automatically logs:
- Request method (GET, POST, etc.)
- Request path
- Response status code
- Request duration in milliseconds

All requests are logged at the INFO level using Python's logging module. Example log output:
```
2024-01-15 10:30:45,123 - app - INFO - Request: GET /hello - Status: 200 - Duration: 15.23 ms
2024-01-15 10:30:46,456 - app - INFO - Request: POST /math - Status: 200 - Duration: 12.78 ms
2024-01-15 10:30:47,789 - app - INFO - Request: POST /math - Status: 400 - Duration: 8.45 ms
```

## Getting Started

### Flask Backend (Python)
To run the Flask backend:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

The API will be available at `http://localhost:5000`

### Express Backend (Node.js)
To run the Express backend:

```bash
# Install dependencies
npm install

# Run the Express app
npm start

# Or for development with auto-reload
npm run dev
```

The API will be available at `http://localhost:3000`

### Testing the Math Endpoint

**Flask (Python):**
```bash
# Test addition
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'

# Test division by zero
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 10, "b": 0}'
```

**Express (Node.js):**
```bash
# Test subtraction
curl -X POST http://localhost:3000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "subtract", "a": 15, "b": 7}'

# Test multiplication
curl -X POST http://localhost:3000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "a": 3.5, "b": 2.5}'
```

### Running Tests

**Flask Tests:**
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Run all Flask tests
pytest -v

# Run specific test files
pytest test_hello.py -v
pytest test_math.py -v
pytest test_logging_middleware.py -v
```

**Node.js Tests:**
```bash
# Run Node.js math endpoint tests
node test_math_node.js
```

**Manual Validation (Flask):**
```bash
# Run manual validation script
python validate_math.py
```

## Project Structure

```
├── index.html                    # Main HTML entry point
├── styles.css                   # All CSS styles
├── app.js                       # JavaScript application logic (frontend)
├── app.py                       # Flask backend application with math endpoint
├── server.js                    # Express backend application with math endpoint
├── test_hello.py                # Unit tests for hello/goodbye endpoints
├── test_math.py                 # Unit tests for math endpoint (Flask)
├── test_math_node.js            # Tests for math endpoint (Node.js)
├── test_logging_middleware.py   # Unit tests for logging middleware
├── validate_math.py             # Manual validation script for math endpoint
├── demo_logging.py              # Demo script to test logging functionality
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
├── pytest.ini                  # Pytest configuration
└── README.md                   # This file
```

## Usage

### Frontend
1. **Create a note**: Enter a title and content in the form fields, then click "Save Note"
2. **View notes**: All saved notes appear as cards in the grid below the form
3. **Delete a note**: Click the × button on any note card to remove it
4. **Keyboard shortcut**: Press `Ctrl/Cmd + Enter` while in the form to quickly save a note

### Math API Usage Examples

**Addition:**
```bash
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 15.5, "b": 4.25}'
```

**Division:**
```bash
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 100, "b": 3}'
```

**Error handling:**
```bash
# Missing field
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10}'

# Invalid operation
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "a": 2, "b": 3}'
```

## Browser Support

Works in all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## Technical Details

- **Frontend Storage**: Uses browser's localStorage API for data persistence
- **Frontend Dependencies**: Pure vanilla JavaScript with no external libraries
- **Backend Options**: 
  - Flask (Python) with comprehensive logging and error handling
  - Express (Node.js) with similar functionality
- **Math Operations**: Support for integers and floating-point numbers
- **Error Handling**: Comprehensive validation and meaningful error messages
- **Testing**: 
  - pytest for Flask unit tests with 17 test cases covering all scenarios
  - Custom Node.js test script for Express endpoint validation
- **Logging**: Python's built-in logging module with INFO level (Flask only)
- **Request Timing**: High-precision timing using `time.time()` for millisecond accuracy
- **Responsive design**: CSS Grid and Flexbox for layout
- **Animations**: CSS animations and transitions for smooth UX

## License

MIT License - Feel free to use and modify as needed.