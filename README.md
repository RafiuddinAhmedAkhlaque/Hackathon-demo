# My Notes App

A simple, clean note-taking web application built with vanilla HTML, CSS, and JavaScript, with both Flask (Python) and Express.js (Node.js) API backends.

## Features

- **Create Notes**: Add notes with a title and body content
- **View Notes**: See all your notes displayed in a responsive grid layout
- **Delete Notes**: Remove notes you no longer need
- **Persistent Storage**: Notes are saved in localStorage and persist across page refreshes
- **Modern UI**: Clean design with smooth animations and transitions
- **Responsive**: Works great on desktop, tablet, and mobile devices
- **Dual API Backends**: Both Flask (Python) and Express.js (Node.js) implementations
- **Request Logging**: Automatic logging of all HTTP requests with timing information (Flask)
- **Timestamp Support**: All API responses include ISO 8601 formatted timestamps

## API Endpoints

All API responses now include a `timestamp` field in ISO 8601 format (e.g., `"2026-02-06T12:30:00Z"`).

### Flask Backend (Python) - Port 5000

#### GET /hello
Returns a simple greeting message with timestamp.

**Response:**
```json
{
  "message": "Hello, World!",
  "timestamp": "2026-02-06T12:30:00Z"
}
```

#### GET /goodbye
Returns a simple farewell message with timestamp.

**Response:**
```json
{
  "message": "Goodbye, World!",
  "timestamp": "2026-02-06T12:30:00Z"
}
```

#### GET /health
Returns health status with timestamp.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-06T12:30:00Z"
}
```

### Express.js Backend (Node.js) - Port 3000

#### GET /hello
Returns a simple greeting message with timestamp.

**Response:**
```json
{
  "message": "Hello, World!",
  "timestamp": "2026-02-06T12:30:00Z"
}
```

#### GET /health
Returns health status with timestamp.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-06T12:30:00Z"
}
```

**Status Code:** 200 for all successful responses

## Timestamp Implementation

Both backends include utility functions to generate consistent ISO 8601 timestamps:

- **Flask**: `generate_timestamp()` function using `datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')`
- **Express.js**: `generateTimestamp()` function using `new Date().toISOString().replace(/\.\d{3}Z$/, 'Z')`

The timestamps are in UTC timezone and follow the format: `YYYY-MM-DDTHH:MM:SSZ`

## Request Logging (Flask Only)

The Flask application includes comprehensive request logging middleware that automatically logs:
- Request method (GET, POST, etc.)
- Request path
- Response status code
- Request duration in milliseconds

All requests are logged at the INFO level using Python's logging module. Example log output:
```
2024-01-15 10:30:45,123 - app - INFO - Request: GET /hello - Status: 200 - Duration: 15.23 ms
2024-01-15 10:30:46,456 - app - INFO - Request: GET /goodbye - Status: 200 - Duration: 12.78 ms
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

### Express.js Backend (Node.js)
To run the Express.js backend:

```bash
# Install dependencies
npm install

# Run the server
npm start

# Or run in development mode
npm run dev
```

The API will be available at `http://localhost:3000`

### Testing the Logging Middleware (Flask)
You can test the logging functionality using the included demo script:

```bash
# Make sure the Flask server is running first (python app.py)
# Then in another terminal:
python demo_logging.py
```

### Running Tests

#### Python Tests (Flask)
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Run all tests
pytest -v

# Run specific test files
pytest test_hello.py -v
pytest test_logging_middleware.py -v
```

#### Node.js Tests (Express.js)
```bash
# Make sure dependencies are installed
npm install

# Run tests
npm test
```

## Project Structure

```
├── index.html                # Main HTML entry point
├── styles.css               # All CSS styles
├── app.js                   # JavaScript application logic (frontend)
├── app.py                   # Flask backend application with logging middleware
├── server.js                # Express.js backend application
├── test_hello.py            # Unit tests for Flask endpoints
├── test_server.js           # Unit tests for Express.js endpoints
├── test_logging_middleware.py # Unit tests for Flask logging middleware
├── demo_logging.py          # Demo script to test Flask logging functionality
├── requirements.txt         # Python dependencies
├── package.json             # Node.js dependencies and scripts
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

#### Flask Backend (Port 5000)
```bash
# Test the hello endpoint
curl http://localhost:5000/hello

# Test the goodbye endpoint
curl http://localhost:5000/goodbye

# Test the health endpoint
curl http://localhost:5000/health
```

#### Express.js Backend (Port 3000)
```bash
# Test the hello endpoint
curl http://localhost:3000/hello

# Test the health endpoint
curl http://localhost:3000/health
```

All responses will include a timestamp field in ISO 8601 format.

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
  - Flask Python web framework (with logging middleware)
  - Express.js Node.js framework
- **Testing**: 
  - pytest for Python unit tests with pytest-flask
  - Jest and supertest for Node.js unit tests
- **Timestamp Format**: ISO 8601 in UTC timezone (`YYYY-MM-DDTHH:MM:SSZ`)
- **Logging**: Python's built-in logging module with INFO level (Flask only)
- **Request Timing**: High-precision timing using `time.time()` for millisecond accuracy (Flask)
- **Responsive design**: CSS Grid and Flexbox for layout
- **Animations**: CSS animations and transitions for smooth UX

## Dependencies

### Python (Flask)
- Flask==2.3.2
- pytest==7.4.0
- pytest-flask==1.2.0
- requests==2.31.0

### Node.js (Express.js)
- express: ^4.18.2
- jest: ^29.0.0 (dev)
- supertest: ^6.3.0 (dev)
- nodemon: ^3.0.1 (dev)

## License

MIT License - Feel free to use and modify as needed.