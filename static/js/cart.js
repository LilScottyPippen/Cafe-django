function addCartItem(elem, productId, csrf_token){
  const itemBtn = elem.parentNode
  itemBtn.querySelector('.section-dishes-item-add-to-cart').remove()

  const span = document.createElement('span');
  span.textContent = 'В корзине';

  itemBtn.appendChild(span)

  addCartItemRequest(productId, csrf_token)
}

function deleteCartItem(elem, product_id, csrf_token, deliveryCost) {
  const row = elem.parentNode.parentNode
  const itemPrice = parseInt(row.querySelector('#itemSum').innerHTML)

  deleteCartItemRequest(product_id, csrf_token)

  if (row.parentNode) {
    row.parentNode.removeChild(row)
  }

  updateCartAmount(itemPrice, deliveryCost)

  if (getCartLength() === 0){
    setEmptyCart()
  }
}

function getCartLength(){
  const tbody = document.querySelector('.section-cart-item')
  const trElements = tbody.getElementsByTagName('tr')

  return trElements.length
}

function setEmptyCart(){
  const parentSection = document.querySelector('.section-container')
  parentSection.innerHTML = ''
  parentSection.innerHTML = '<section class="section-cart"><span class="section-title">КОРЗИНА</span><span>Корзина пуста.</span></section>'
}

function updateCartAmount(itemPrice, deliveryCost){
  let cartAmount = parseInt(document.getElementById('cart-amount').innerHTML)
  let amount = cartAmount - itemPrice

  document.getElementById('cart-amount').innerHTML = amount.toString()
  updateCartTotalAmount(deliveryCost)
}

function updateCartTotalAmount(deliveryCost){
  const cartAmount = parseInt(document.getElementById('cart-amount').innerHTML)
  document.getElementById('cart-total-amount').innerHTML = (cartAmount + deliveryCost).toString()
}