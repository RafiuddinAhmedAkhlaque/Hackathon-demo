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

/**
 * POST /echo - Echo endpoint that returns the input message with metadata
 * Accepts JSON body with 'message' field and returns it with computed metadata
 */
app.post('/echo', (req, res) => {
    try {
        // Check if message field is present
        if (!req.body || typeof req.body.message === 'undefined') {
            return res.status(400).json({
                error: "Missing 'message' field in request body"
            });
        }

        const message = req.body.message;

        // Check if message is a string
        if (typeof message !== 'string') {
            return res.status(400).json({
                error: "'message' field must be a string"
            });
        }

        // Calculate metadata
        const characterCount = message.length;
        const wordCount = message.trim() ? message.split(/\s+/).length : 0;
        const reversed = message.split('').reverse().join('');
        const uppercase = message.toUpperCase();
        const timestamp = new Date().toISOString();

        // Return response with metadata
        const response = {
            original_message: message,
            character_count: characterCount,
            word_count: wordCount,
            reversed: reversed,
            uppercase: uppercase,
            timestamp: timestamp
        };

        res.status(200).json(response);

    } catch (error) {
        console.error('Error processing echo request:', error);
        res.status(500).json({
            error: "Internal server error"
        });
    }
});

// Serve the main HTML file for the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Try the hello endpoint: http://localhost:${PORT}/hello`);
    console.log(`Try the echo endpoint: POST http://localhost:${PORT}/echo`);
});

module.exports = app;