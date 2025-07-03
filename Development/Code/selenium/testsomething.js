const {expect, should} = require('chai')

function testchai () {
    let somearray = [];
    const i = somearray.push(1, 2, 3, 4, 5);

    
}

testchai ();

function slicearray () {
    let somearray = [];
    
    const a = somearray.push(2)
    

    let slicedarray = somearray.slice(3)

    expect(slicearray[1]).to.equal(2); 

}

slicearray();
