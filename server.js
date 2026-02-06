const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname)));

// API Routes

/**
 * GET /hello - Hello World endpoint
 * Returns a JSON response with a greeting message
 */
app.get('/hello', (req, res) => {
    res.status(200).json({
        message: "Hello, World!"
    });
});

// Serve the main HTML file for the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Try the hello endpoint: http://localhost:${PORT}/hello`);
});

module.exports = app;