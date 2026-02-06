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
- **API Backend**: Flask backend with hello endpoint

## Getting Started

### Frontend Only
Simply open `index.html` in your web browser. No build tools or server required!
- **API Endpoints**: RESTful API for programmatic access

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

## Getting Started

### Prerequisites
- Node.js (version 14 or higher)
- npm (comes with Node.js)

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
To run the Flask backend with the hello endpoint:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

The API will be available at `http://localhost:5000`

### Running Tests
To run the unit tests for the hello endpoint:

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
├── test_hello.py   # Unit tests for hello endpoint
├── requirements.txt # Python dependencies
├── pytest.ini     # Pytest configuration
└── README.md       # This file
4. Open your browser and visit `http://localhost:3000`

### Development Mode

For development with auto-reload:
```bash
npm run dev
```

## Testing the API

You can test the API endpoints using curl or any HTTP client:

```bash
# Test the hello endpoint
curl http://localhost:3000/hello
```

Or visit `http://localhost:3000/hello` directly in your browser.

## Project Structure

```
├── index.html     # Main HTML entry point
├── styles.css     # All CSS styles
├── app.js         # Frontend JavaScript application logic
├── server.js      # Express.js server with API endpoints
├── package.json   # Node.js project configuration
└── README.md      # This file
```

## API Endpoints

- `GET /hello` - Returns a hello world message

## Usage

1. **Create a note**: Enter a title and content in the form fields, then click "Save Note"
2. **View notes**: All saved notes appear as cards in the grid below the form
3. **Delete a note**: Click the × button on any note card to remove it
4. **Keyboard shortcut**: Press `Ctrl/Cmd + Enter` while in the form to quickly save a note
5. **API Access**: Use the `/hello` endpoint to get a programmatic greeting

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
- **Frontend**: Pure vanilla JavaScript with no external libraries
- **Backend**: Express.js server for API endpoints
- **Storage**: Uses browser's localStorage API for data persistence (frontend)
- **Responsive design**: CSS Grid and Flexbox for layout
- **Animations**: CSS animations and transitions for smooth UX

## License

MIT License - Feel free to use and modify as needed.