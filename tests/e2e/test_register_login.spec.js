const { test, expect } = require('@playwright/test');

test.describe('User Registration & Login API', () => {

  test('Positive: Register and login with valid data', async ({ request }) => {
    const email = `user${Date.now()}@example.com`;
    const password = "testpass123";

    // Register
    const registerResponse = await request.post('http://127.0.0.1:8000/register', {
      data: { email, username: email, password }
    });
    expect(registerResponse.status()).toBe(200);
    const registerData = await registerResponse.json();
    expect(registerData.access_token).not.toBeNull();

    // Login
    const loginResponse = await request.post('http://127.0.0.1:8000/login', {
      data: { username: email, password }
    });
    expect(loginResponse.status()).toBe(200);
    const loginData = await loginResponse.json();
    expect(loginData.access_token).not.toBeNull();
  });

  test('Negative: Login with wrong password', async ({ request }) => {
    const email = `user${Date.now()}@example.com`;
    const correctPassword = "testpass123";
    const wrongPassword = "wrongpass456";

    // Register
    await request.post('http://127.0.0.1:8000/register', {
      data: { email, username: email, password: correctPassword }
    });

    // Login with wrong password
    const loginResponse = await request.post('http://127.0.0.1:8000/login', {
      data: { username: email, password: wrongPassword }
    });
    expect(loginResponse.status()).toBe(401);
    const data = await loginResponse.json();
    expect(data.detail).toBe('Invalid credentials');
  });

});
