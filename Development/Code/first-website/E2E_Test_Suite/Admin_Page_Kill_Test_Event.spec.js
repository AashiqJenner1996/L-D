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
    if (url.includes(ADMIN_URL)) {
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

test('kill event', async ({ page }) => {
  console.log('🔐 Navigating to admin panel...');
  await page.goto(ADMIN_URL, { waitUntil: 'load' });

  try {
    console.log('🔑 Logging in...');
    await page.getByPlaceholder('Enter your email address').click();
    await page.getByPlaceholder('Enter your email address').fill(email);
    await page.getByRole('button', { name: 'Continue' }).click();
    await page.getByPlaceholder('Enter your password').fill(password);
    await page.getByRole('button', { name: 'Continue' }).click();
    console.log('✅ Login successful');
  } catch (err) {
    console.error('❌ Login failed:', err);
    throw err;
  }

  try {
    console.log('📅 Deleting event...');
    await page.getByRole('button', { name: 'No Project' }).click()
    await page.getByRole('menuitem', { name: 'Demo' }).click();
    await expect(page.getByRole('link', { name: 'test event' })).toBeVisible();
    await page.getByRole('link', { name: 'test event' }).click({timeout:10000});
    await expect(
      page.locator('span[role="link"][aria-current="page"]', { hasText: 'test event' })
    ).toBeVisible();    
    await page.getByRole('link', { name: 'Danger Zone' }).click();
    await page.getByRole('button', { name: 'Delete' }).click();   
    await page.getByRole('button', { name: 'Continue' }).click();   
    console.log('✅ Event deleted');
  } catch (err) {
    console.error('❌ Event deletion failed:', err);
    throw err;
  }
});