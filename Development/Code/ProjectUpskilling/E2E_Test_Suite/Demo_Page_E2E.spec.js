const { test, expect } = require('@playwright/test');
require("dotenv").config();

const ADMIN_URL = process.env.admin_url;
const DEMO_URL = process.env.demo_url;
const vercelbypass = process.env.vercelbypass
const password = process.env.password
const email = process.env.email

test.beforeEach(async ({ page }) => {
  await page.route('**/*', (route) => {
    const url = route.request().url();
    if (url.includes(DEMO_URL)) {
      route.continue({
        headers: {
          ...route.request().headers(),
          'x-vercel-protection-bypass': vercelbypass,
        },
      });
    } else {
      route.continue();
    }
  });
});


test('demo page', async ({ page, context }) => {
    try {
      console.log('🌐 Navigating to DEMO_URL...');
      await page.goto(DEMO_URL);
      console.log('✅ Page loaded');
    } catch (err) {
      console.error('❌ Failed to load DEMO_URL:', err);
      throw err;
    }
  
    try {
      console.log('🔗 Navigating to test event via View Pricing...');
      await page.getByRole('link', { name: 'View Pricing' }).click();
      await page.getByRole('link', { name: 'test event' }).click();
      console.log('✅ Event selected');
    } catch (err) {
      console.error('❌ Failed to select event:', err);
      throw err;
    }
  
    try {
      console.log('🔑 Logging in...');
      await page.getByPlaceholder('Enter your email address').click();
      await page.getByPlaceholder('Enter your email address').fill(email);
      await page.getByRole('button', { name: 'Continue' }).click();
      await page.getByPlaceholder('Enter your password').fill(password);
      await page.getByRole('button', { name: 'Continue' }).click();
      console.log('✅ Login complete');
    } catch (err) {
      console.error('❌ Login failed:', err);
      throw err;
    }
  
    try {
      console.log('🎫 buy ticket');
      await page.getByRole('button', { name: 'Buy Ticket' }).click();
      console.log('✅ buy ticket complete');
    } catch (err) {
      console.error('❌ Failed to buy ticket:', err);
      throw err;
    }
  
  
    try {
      console.log('💬 Sending chat message...');
      await page.getByPlaceholder('Enter a message...').fill('Hello world!');
      await page.keyboard.press('Enter');
      console.log('✅ Message sent');
    } catch (err) {
      console.error('❌ Failed to send message:', err);
      throw err;
    }
  
    try {
      console.log('🎮 Joining pixel stream...');
      const [streamPage] = await Promise.all([
        context.waitForEvent('page'),
        page.getByRole('button', { name: 'Join Pixel Stream' }).click(),
      ]);
      await streamPage.waitForLoadState('load', { timeout: 10000 });
      console.log('✅ Pixel stream joined and loaded');
    } catch (err) {
      console.error('❌ Failed to join pixel stream:', err);
      throw err;
    }
  });