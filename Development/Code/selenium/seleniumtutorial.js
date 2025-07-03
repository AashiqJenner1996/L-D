const { WebDriver, Builder, By } = require("selenium-webdriver");
const { ChromiumWebDriver } = require("selenium-webdriver/chromium");
const assert = require('assert');
const expect = require('chai').expect();
const Should = require('chai').Should();





async function logintest() {
 let driver = new Builder().forBrowser('chrome').build();
 console.log('typing on page')
 try{
    const page = "https://onlinenotepad.org/notepad"

    await driver.get(page);

    const selectIframe = await driver.findElement(By.css('#editor_ifr'))

    await driver.switchTo().frame(selectIframe);

    const edittext = await driver.findElement(By.css('#tinymce'))

    await edittext.sendKeys('test')

    const findText = await driver.findElement(By.css('#tinymce')).getText();

    if(findText.includes('test')){
        console.log('it does');
    } else {
        console.log('not there')
    }     

} catch (err) {
    console.error("Error:", err)
} 

finally {
    await driver.quit();
}
};

logintest();

