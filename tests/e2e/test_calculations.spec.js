const { test, expect } = require('@playwright/test');

test.describe('Calculation API', () => {

  test('Positive: Create calculation with valid data', async ({ request }) => {
    const email = `calcuser${Date.now()}@example.com`;
    const password = 'testpass123';

    // Register user
    const registerResponse = await request.post('http://127.0.0.1:8000/register', {
      data: { email, username: email, password }
    });
    expect(registerResponse.status()).toBe(200);
    const registerData = await registerResponse.json();
    const token = registerData.access_token;
    expect(token).not.toBeNull();

    // Create calculation
    const response = await request.post('http://127.0.0.1:8000/calculations', {
      data: { a: 10, b: 5, type: 'add' },
      headers: { 'Authorization': `Bearer ${token}` }
    });

    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data).toHaveProperty('id');
    expect(data.result).toBe(15);
    expect(data.type).toBe('ADD');
  });

  test('Negative: Create calculation without token', async ({ request }) => {
    const response = await request.post('http://127.0.0.1:8000/calculations', {
      data: { a: 10, b: 5, type: 'add' }
    });

    expect(response.status()).toBe(401);
    const data = await response.json();
    expect(data.detail).toBe('Not authenticated');
  });

  test('Negative: Create calculation with invalid type', async ({ request }) => {
    const email = `calcuser${Date.now()}@example.com`;
    const password = 'testpass123';

    // Register user
    await request.post('http://127.0.0.1:8000/register', {
      data: { email, username: email, password }
    });

    // Login to get token
    const loginResponse = await request.post('http://127.0.0.1:8000/login', {
      data: { username: email, password }
    });
    expect(loginResponse.status()).toBe(200);
    const token = (await loginResponse.json()).access_token;
    expect(token).not.toBeNull();

    // Invalid type
    const response = await request.post('http://127.0.0.1:8000/calculations', {
      data: { a: 5, b: 3, type: 'invalid_op' },
      headers: { 'Authorization': `Bearer ${token}` }
    });

    // Pydantic validation fails
    expect(response.status()).toBe(422);
    const respData = await response.json();
    expect(respData.detail).toBeDefined();
  });

});
