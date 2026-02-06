const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname)));

/**
 * Generate ISO 8601 formatted timestamp in UTC
 * @returns {string} ISO 8601 formatted timestamp (e.g., "2026-02-06T12:30:00Z")
 */
function generateTimestamp() {
    return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

// API Routes

/**
 * GET /hello - Hello World endpoint
 * Returns a JSON response with a greeting message and timestamp
 */
app.get('/hello', (req, res) => {
    res.status(200).json({
        message: "Hello, World!",
        timestamp: generateTimestamp()
    });
});

/**
 * GET /health - Health check endpoint
 * Returns a JSON response with health status and timestamp
 */
app.get('/health', (req, res) => {
    res.status(200).json({
        status: "healthy",
        timestamp: generateTimestamp()
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
    console.log(`Try the health endpoint: http://localhost:${PORT}/health`);
});

module.exports = app;