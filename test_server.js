/**
 * Unit tests for the Express.js server endpoints
 * Run with: npm test (after adding test script to package.json)
 */

const request = require('supertest');
const app = require('./server');

describe('API Endpoints', () => {
    
    describe('GET /hello', () => {
        it('should return 200 status code', async () => {
            const response = await request(app).get('/hello');
            expect(response.status).toBe(200);
        });

        it('should return Hello, World! message', async () => {
            const response = await request(app).get('/hello');
            expect(response.body.message).toBe('Hello, World!');
        });

        it('should include timestamp field', async () => {
            const response = await request(app).get('/hello');
            expect(response.body).toHaveProperty('timestamp');
        });

        it('should have timestamp in ISO 8601 format', async () => {
            const response = await request(app).get('/hello');
            const timestamp = response.body.timestamp;
            const isoPattern = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
            expect(timestamp).toMatch(isoPattern);
        });
    });

    describe('GET /health', () => {
        it('should return 200 status code', async () => {
            const response = await request(app).get('/health');
            expect(response.status).toBe(200);
        });

        it('should return healthy status', async () => {
            const response = await request(app).get('/health');
            expect(response.body.status).toBe('healthy');
        });

        it('should include timestamp field', async () => {
            const response = await request(app).get('/health');
            expect(response.body).toHaveProperty('timestamp');
        });

        it('should have timestamp in ISO 8601 format', async () => {
            const response = await request(app).get('/health');
            const timestamp = response.body.timestamp;
            const isoPattern = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
            expect(timestamp).toMatch(isoPattern);
        });
    });

    describe('Timestamp consistency', () => {
        it('should generate different timestamps for subsequent calls', async () => {
            const response1 = await request(app).get('/hello');
            // Small delay to ensure different timestamps
            await new Promise(resolve => setTimeout(resolve, 1000));
            const response2 = await request(app).get('/hello');
            
            expect(response1.body.timestamp).not.toBe(response2.body.timestamp);
        });
    });
});