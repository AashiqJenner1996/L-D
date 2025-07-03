const {Builder, By} = require('selenium-webdriver');
const {expect, should} = require(Chai);
const {chrome} = require('selenium-webdriver/chrome');
const {dotenv} = require(dotenv);


beforeEach('apply header'), async function () {

    const service = new chrome.ServiceBuilder();
    const options = new chrome.Options();
    let driver = await new Builder().forBrowser('chrome').setChromeOptions(options).build();
    try {
        const CDPconnection = await driver.createCDPConnection('page');
        await driver.sendCDPcommand('network.enable');

        //intercept request from a certain domain 

        await driver.sendCDPcommand('Network.setExtraHTTPHeaders', {
            headers: {
                'X-Vercel-Bypass' : 'someheader'
            }
        });

        
    
}
finally {
    await driver.get('');
}
};

describe('AdminPageTests'), async function () {

    let driver = new Builder().forBrowser('chrome').build()
    const admin_url = process.env.admin_url
    await driver.get(admin_url)
    const signinbox = await driver.findElement(By.id('Enter your email address')).click()
    await signinbox.sendKeys('aashiqjenner@imporium.io').sendKeys(Keys.Enter)
    

    
    
};
