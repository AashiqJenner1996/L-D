const {Builder, By, until} = require('selenium-webdriver');
const {expect} = require('chai');
let driver = new Builder().forBrowser('chrome').build();

describe ("some tests", function() {

    this.timeout(20000); // 20 seconds


    before(async function () {
        await driver.get('https://onlinenotepad.org/notepad');
    });

    after(async function () {

        await driver.quit();
        
    });

    it("some test", async function () {

   
        const selectIframecss = await driver.findElement(By.css('#editor_ifr')); // i have to switch to the iframe first because it has it's own DOM

        await driver.switchTo().frame(selectIframecss);

        const selecttextarea = await driver.findElement(By.css('#tinymce')); // now i can find the text box 

        await selecttextarea.sendKeys('test'); 

        const textareacontent = await selecttextarea.getText();

        expect(textareacontent).to.include("test");


    
    });

    it("another test", async function () {

        // const selectdropdown = await driver.findElement(By.css('#mceu_14'), 5000); // find the file button 

        // selectdropdown.click(); // click the file button 

        const dropdowncontents = await driver.wait(until.elementLocated(By.css("#mceu_14")), 5000); // define what we're looking for 

        await driver.wait(until.elementisVisbile(dropdowncontents), 50000); // wait for it to appear 

        const getdropdowntext = await dropdowncontents.getText();

        expect(getdropdowntext).to.include("File")

        
    })



});






