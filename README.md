# My Notes App

A simple, clean note-taking web application built with vanilla HTML, CSS, and JavaScript, with a Flask API backend.
A simple, clean note-taking web application built with vanilla HTML, CSS, and JavaScript, now with Express.js backend API.

## Features

- **Create Notes**: Add notes with a title and body content
- **View Notes**: See all your notes displayed in a responsive grid layout
- **Delete Notes**: Remove notes you no longer need
- **Persistent Storage**: Notes are saved in localStorage and persist across page refreshes
- **Modern UI**: Clean design with smooth animations and transitions
- **Responsive**: Works great on desktop, tablet, and mobile devices
- **API Backend**: Flask backend with hello and health endpoints

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

### GET /health
Returns the health status of the application with system information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456Z",
  "version": "1.0.0"
}
```

**Status Code:** 200

**Response Fields:**
- `status`: Current health status of the application (always "healthy")
- `timestamp`: Current UTC timestamp in ISO format
- `version`: Application version number

## Getting Started

### Prerequisites
- Node.js (version 14 or higher)
- npm (comes with Node.js)
- Python 3.7+ (for Flask backend)

### Installation

1. Clone or download the repository
2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

### Backend API
To run the Flask backend with the API endpoints:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

The API will be available at `http://localhost:5000`

### Running Tests
To run the unit tests for the API endpoints:

```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Run tests with pytest
pytest test_hello.py -v
```

## Project Structure

```
├── index.html      # Main HTML entry point
├── styles.css      # All CSS styles
├── app.js          # JavaScript application logic (frontend)
├── app.py          # Flask backend application
├── test_hello.py   # Unit tests for API endpoints
├── requirements.txt # Python dependencies
├── pytest.ini     # Pytest configuration
└── README.md       # This file
```

## Testing the API

You can test the API endpoints using curl or any HTTP client:

```bash
# Test the hello endpoint
curl http://localhost:5000/hello

# Test the health endpoint
curl http://localhost:5000/health
```

Or visit the endpoints directly in your browser:
- `http://localhost:5000/hello`
- `http://localhost:5000/health`

## Usage

1. **Create a note**: Enter a title and content in the form fields, then click "Save Note"
2. **View notes**: All saved notes appear as cards in the grid below the form
3. **Delete a note**: Click the × button on any note card to remove it
4. **Keyboard shortcut**: Press `Ctrl/Cmd + Enter` while in the form to quickly save a note
5. **API Access**: Use the `/hello` and `/health` endpoints for programmatic access

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
- **Testing**: pytest for unit tests
- **Responsive design**: CSS Grid and Flexbox for layout
- **Animations**: CSS animations and transitions for smooth UX

## License

MIT License - Feel free to use and modify as needed.