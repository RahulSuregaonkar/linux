
    
onLoadCartNumbers();
let cart = document.querySelectorAll('.d-flex');
let products = [{
  name: "book 1",
  tag: "book-1",
  price : 1777,
  inCart: 0,
  content: "hey "

}]


for (let i = 0; i <= cart.length; i++ ){
  console.log('my loop ');
  cart[i].addEventListener('click',() => {
    cartNumber(products[i]);
    totalCost(products[i]);
  })



}

function onLoadCartNumbers() {
  let productNumbers = localStorage.getItem('cartNumbers');

  if(productNumbers) {
    document.querySelector('.icons span').textContent = productNumbers;

  }


}
function setItems(product) {
  let cartItems = localStorage.getItem('productsInCart');
  cartItems = JSON.parse(cartItems);

  console.log("My cart items are ",cartItems);
  
  if(cartItems != null){
    
    if(cartItems[product.tag] == undefined){
      cartItems = {
        ...cartItems,
        [product.tag]: product
      }
    }
    cartItems[product.tag].inCart += 1;
  }else{product.inCart = 1;
    cartItems = {
      [product.tag]: product

    }
    
  }
  
  localStorage.setItem("productsInCart", JSON.stringify(cartItems));



}



function cartNumber(product) {
  
  let productNumbers = localStorage.getItem('cartNumbers');
  
  productNumbers = parseInt(productNumbers);
  console.log(typeof productNumbers);
  console.log(productNumbers);

  if (productNumbers ){
    localStorage.setItem('cartNumbers',productNumbers +1);
    document.querySelector('.icons span').textContent = productNumbers + 1;
  } else {
    localStorage.setItem('cartNumbers',1)
    document.querySelector('.icons span').textContent = 1;

  }

  setItems(product);
}

function totalCost(product){
  
  let cartCost = localStorage.getItem('totalCost');
  
  console.log(cartCost)
  console.log(typeof cartCost);

  if(cartCost != null){
    cartCost =parseInt(cartCost);

    localStorage.setItem("totalCost", cartCost + product.price);

  }else{
    localStorage.setItem("totalCost",product.price);
  }


  

}




onLoadCartNumbers();
let cart = document.querySelectorAll('.addToBagp');
let products = [{
name: "book 1",
tag: "book-1",
price : 1777,
inCart: 0,
content: "hey "

},
{
name: "book 2",
tag: "book-2",
price : 1777,
inCart: 0,
content: "hey "

},
{
name: "book 3",
tag: "book-3",
price : 1777,
inCart: 0,
content: "hey "

},
{
name: "book 4",
tag: "book-4",
price : 1777,
inCart: 0,
content: "hey "

}, {
name: "book 5",
tag: "book-5",
price : 1777,
inCart: 0,
content: "hey "

}, {
name: "book 6",
tag: "book-6",
price : 1777,
inCart: 0,
content: "hey "

}, {
name: "book 7",
tag: "book-7",
price : 1777,
inCart: 0,
content: "hey "

}, {
name: "book 8",
tag: "book-8",
price : 1777,
inCart: 0,
content: "hey "

}]


for (let i = 0; i <= cart.length; i++ ){
console.log('my loop ');
cart[i].addEventListener('click',() => {
cartNumber(products[i]);
totalCost(products[i]);
})



}

function onLoadCartNumbers() {
let productNumbers = localStorage.getItem('cartNumbers');

if(productNumbers) {
document.querySelector('.icons span').textContent = productNumbers;

}


}
function setItems(product) {
let cartItems = localStorage.getItem('productsInCart');
cartItems = JSON.parse(cartItems);

console.log("My cart items are ",cartItems);

if(cartItems != null){

if(cartItems[product.tag] == undefined){
  cartItems = {
    ...cartItems,
    [product.tag]: product
  }
}
cartItems[product.tag].inCart += 1;
}else{product.inCart = 1;
cartItems = {
  [product.tag]: product

}

}

localStorage.setItem("productsInCart", JSON.stringify(cartItems));



}



function cartNumber(product) {

let productNumbers = localStorage.getItem('cartNumbers');

productNumbers = parseInt(productNumbers);
console.log(typeof productNumbers);
console.log(productNumbers);

if (productNumbers ){
localStorage.setItem('cartNumbers',productNumbers +1);
document.querySelector('.icons span').textContent = productNumbers + 1;
} else {
localStorage.setItem('cartNumbers',1)
document.querySelector('.icons span').textContent = 1;

}

setItems(product);
}

function totalCost(product){

let cartCost = localStorage.getItem('totalCost');

console.log(cartCost)
console.log(typeof cartCost);

if(cartCost != null){
cartCost =parseInt(cartCost);

localStorage.setItem("totalCost", cartCost + product.price);

}else{
localStorage.setItem("totalCost",product.price);
}




}


