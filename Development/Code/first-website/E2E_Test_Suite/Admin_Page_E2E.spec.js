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

test('admin panel', async ({ page }) => {
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
    
  }

  try {
    console.log('📅 Creating event...');
    await page.getByRole('button', { name: 'No Project' }).click();
    await page.getByRole('menuitem', { name: 'Demo' }).click();
    await page.getByRole('button', { name: 'Create Event' }).click();
    await page.getByPlaceholder('Event name').fill('test event');
    await page.getByRole('button', { name: 'Create' }).click();
    console.log('✅ Event created');
  } catch (err) {
    console.error('❌ Event creation failed:', err);
    
  }

  try {
    console.log('🎟️ Creating ticket...');
    await page.getByRole('link', { name: 'Tickets' }).click();
    await page.getByRole('button', { name: 'Create Ticket' }).click();
    await page.getByPlaceholder('Ticket X').fill('some test text');
    await page.getByPlaceholder('Enter a description...').fill('This is a test description.');
    await page.getByRole('switch', { name: 'Limited Quantity' }).click();
    await page.getByRole('switch', { name: 'Allow World Access' }).click();
    await page.locator('input[type="number"]').nth(1).fill('100'); // ideally fix this later
    await page.getByRole('button', { name: 'Create' }).click();
    console.log('✅ Ticket created');
  } catch (err) {
    console.error('❌ Ticket creation failed:', err);
    
  }

  // try {
  //   console.log('📹 Creating cameras...');
  //   await expect(page.getByRole('link', { name: 'Cameras' })).toBeVisible({ timeout: 10000 });
  //   await page.getByRole('link', { name: 'Cameras' }).click();
  
  //   await expect(page.getByRole('button', { name: 'Add Camera' })).toBeVisible({ timeout: 10000 });
  //   await page.getByRole('button', { name: 'Add Camera' }).click();
  
  //   await expect(page.getByPlaceholder('Camera X')).toBeVisible();
  //   await page.getByPlaceholder('Camera X').fill('Test Camera RTMP');
  //   await page.getByRole('button', { name: 'Create' }).click();
  
  //   await expect(page.getByRole('button', { name: 'Add Camera' })).toBeVisible();
  //   await page.getByRole('button', { name: 'Add Camera' }).click();
  
  //   await expect(page.locator('select')).toBeVisible();
  //   await page.locator('select').selectOption('whip');
  //   await page.getByPlaceholder('Camera X').fill('Test Camera WHIP');
  //   await page.getByRole('button', { name: 'Create' }).click();
  
  //   console.log('✅ Cameras created');
  // } catch (err) {
  //   console.error('❌ Camera creation failed:', err);
  // }
  
  

  try {
    console.log('🌍 Linking world...');
    await page.getByRole('link', { name: 'World' }).click();
    await page.getByRole('button', { name: 'Link World' }).click({ timeout: 5000 });   
    await page.locator('option[value="fancy-pants-know-847218"]').waitFor({ state: 'attached', timeout: 10000 });
    await page.locator('select').selectOption('fancy-pants-know-847218');
    await page.getByRole('button', { name: 'Link' }).click();
    console.log('✅ World linked');
  } catch (err) {
    console.error('❌ World linking failed:', err);
     
  }
});

