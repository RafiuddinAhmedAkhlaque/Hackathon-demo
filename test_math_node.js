/**
 * Simple test script for the Node.js math endpoint
 * Run with: node test_math_node.js
 */
const http = require('http');
const assert = require('assert');

// Start the server for testing
const app = require('./server.js');
const PORT = 3001; // Use different port for testing

const server = app.listen(PORT, () => {
    console.log('Test server running on port', PORT);
    runTests();
});

function makeRequest(data, callback) {
    const postData = JSON.stringify(data);
    
    const options = {
        hostname: 'localhost',
        port: PORT,
        path: '/math',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        }
    };

    const req = http.request(options, (res) => {
        let responseBody = '';
        res.on('data', (chunk) => {
            responseBody += chunk;
        });
        res.on('end', () => {
            callback(res.statusCode, JSON.parse(responseBody));
        });
    });

    req.on('error', (e) => {
        console.error('Request error:', e);
    });

    req.write(postData);
    req.end();
}

function runTests() {
    console.log('Running Node.js math endpoint tests...');
    
    let testsCompleted = 0;
    const totalTests = 5;
    
    // Test addition
    makeRequest({
        operation: 'add',
        a: 10,
        b: 5
    }, (statusCode, response) => {
        assert.strictEqual(statusCode, 200);
        assert.strictEqual(response.result, 15);
        console.log('✓ Addition test passed');
        testsCompleted++;
        checkAllTestsCompleted();
    });
    
    // Test division by zero
    makeRequest({
        operation: 'divide',
        a: 10,
        b: 0
    }, (statusCode, response) => {
        assert.strictEqual(statusCode, 400);
        assert.strictEqual(response.error, 'Cannot divide by zero');
        console.log('✓ Division by zero test passed');
        testsCompleted++;
        checkAllTestsCompleted();
    });
    
    // Test invalid operation
    makeRequest({
        operation: 'power',
        a: 2,
        b: 3
    }, (statusCode, response) => {
        assert.strictEqual(statusCode, 400);
        assert(response.error.includes('Unsupported operation'));
        console.log('✓ Invalid operation test passed');
        testsCompleted++;
        checkAllTestsCompleted();
    });
    
    // Test missing field
    makeRequest({
        operation: 'add',
        a: 10
    }, (statusCode, response) => {
        assert.strictEqual(statusCode, 400);
        assert.strictEqual(response.error, 'Missing required field: b');
        console.log('✓ Missing field test passed');
        testsCompleted++;
        checkAllTestsCompleted();
    });
    
    // Test decimal numbers
    makeRequest({
        operation: 'multiply',
        a: 2.5,
        b: 4.2
    }, (statusCode, response) => {
        assert.strictEqual(statusCode, 200);
        assert.strictEqual(response.result, 10.5);
        console.log('✓ Decimal numbers test passed');
        testsCompleted++;
        checkAllTestsCompleted();
    });
    
    function checkAllTestsCompleted() {
        if (testsCompleted === totalTests) {
            console.log('\n🎉 All Node.js tests passed!');
            server.close(() => {
                process.exit(0);
            });
        }
    }
}