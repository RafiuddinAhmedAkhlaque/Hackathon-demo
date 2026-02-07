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
 * POST /math - Math calculator endpoint
 * Performs basic arithmetic operations (add, subtract, multiply, divide)
 * Request body: { "operation": "add", "a": 10, "b": 5 }
 * Returns: { "operation": "add", "a": 10, "b": 5, "result": 15 }
 */
app.post('/math', (req, res) => {
    const { operation, a, b } = req.body;
    
    // Validate required fields
    if (operation === undefined) {
        return res.status(400).json({ error: 'Missing required field: operation' });
    }
    
    if (a === undefined) {
        return res.status(400).json({ error: 'Missing required field: a' });
    }
    
    if (b === undefined) {
        return res.status(400).json({ error: 'Missing required field: b' });
    }
    
    // Validate operation type
    const supportedOperations = ['add', 'subtract', 'multiply', 'divide'];
    if (!supportedOperations.includes(operation)) {
        return res.status(400).json({ 
            error: `Unsupported operation. Supported operations: ${supportedOperations.join(', ')}` 
        });
    }
    
    // Validate that a and b are numbers
    const numA = Number(a);
    const numB = Number(b);
    
    if (isNaN(numA) || isNaN(numB)) {
        return res.status(400).json({ error: "Fields 'a' and 'b' must be valid numbers" });
    }
    
    // Perform the calculation
    let result;
    try {
        switch (operation) {
            case 'add':
                result = numA + numB;
                break;
            case 'subtract':
                result = numA - numB;
                break;
            case 'multiply':
                result = numA * numB;
                break;
            case 'divide':
                if (numB === 0) {
                    return res.status(400).json({ error: 'Cannot divide by zero' });
                }
                result = numA / numB;
                break;
        }
    } catch (error) {
        return res.status(400).json({ error: `Calculation error: ${error.message}` });
    }
    
    // Return the response
    res.status(200).json({
        operation: operation,
        a: numA,
        b: numB,
        result: result
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
    console.log(`Try the math endpoint: POST http://localhost:${PORT}/math`);
});

module.exports = app;