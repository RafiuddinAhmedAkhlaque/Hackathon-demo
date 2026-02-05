# My Notes App

A simple, clean note-taking web application built with vanilla HTML, CSS, and JavaScript.

## Features

- **Create Notes**: Add notes with a title and body content
- **View Notes**: See all your notes displayed in a responsive grid layout
- **Delete Notes**: Remove notes you no longer need
- **Persistent Storage**: Notes are saved in localStorage and persist across page refreshes
- **Modern UI**: Clean design with smooth animations and transitions
- **Responsive**: Works great on desktop, tablet, and mobile devices

## Getting Started

Simply open `index.html` in your web browser. No build tools or server required!

```bash
# Option 1: Open directly in browser
open index.html

# Option 2: Use a simple HTTP server (optional)
python -m http.server 8000
# Then visit http://localhost:8000
```

## Project Structure

```
├── index.html    # Main HTML entry point
├── styles.css    # All CSS styles
├── app.js        # JavaScript application logic
└── README.md     # This file
```

## Usage

1. **Create a note**: Enter a title and content in the form fields, then click "Save Note"
2. **View notes**: All saved notes appear as cards in the grid below the form
3. **Delete a note**: Click the × button on any note card to remove it
4. **Keyboard shortcut**: Press `Ctrl/Cmd + Enter` while in the form to quickly save a note

## Browser Support

Works in all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## Technical Details

- **Storage**: Uses browser's localStorage API for data persistence
- **No dependencies**: Pure vanilla JavaScript with no external libraries
- **Responsive design**: CSS Grid and Flexbox for layout
- **Animations**: CSS animations and transitions for smooth UX

## License

MIT License - Feel free to use and modify as needed.
