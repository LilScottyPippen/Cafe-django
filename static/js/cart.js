function addCartItem(elem, productId, csrf_token){
  const itemBtn = elem.parentNode
  itemBtn.querySelector('.section-dishes-item-add-to-cart').remove()

  const span = document.createElement('span')
  span.classList.add('section-dishes-item-added-to-cart')
  span.textContent = 'В корзине'

  itemBtn.appendChild(span)

  addCartItemRequest(productId, csrf_token)
}

function deleteCartItem(elem, product_id, csrf_token) {
  const row = elem.parentNode.parentNode
  const result = deleteCartItemRequest(product_id, csrf_token)

  if (row.parentNode)
    row.parentNode.removeChild(row)

  result.then(function(json){
    updateCartAmount()

    if (json.items.length === 0)
      setEmptyCart()
  })
}

function setEmptyCart(){
  const parentSection = document.querySelector('.section-container')
  parentSection.innerHTML = '<section class="section-cart"><span class="section-title">КОРЗИНА</span><span>Корзина пуста.</span></section>'
}

function updateCartAmount(){
  const result = getCartAmountRequest()

  result.then(function(json){
    document.getElementById('cart-amount').innerText = json.amount.toString()
    updateCartTotalAmount()
  })
}

function updateCartTotalAmount(){
  const cartAmount = parseInt(document.getElementById('cart-amount').innerHTML)
  const deliveryCost = parseInt(document.getElementById('delivery-cost').innerHTML)
  const discount = parseInt(document.getElementById('discount').innerHTML)
  const cartDiscount = Math.ceil(cartAmount / 100 * discount)

  document.getElementById('cart-total-amount').innerText = cartAmount - cartDiscount + deliveryCost
}

let inputValue

function updateQuantityItemCart(event){
  const inputElement = event.target
  let value = inputElement.value
  const productId = inputElement.dataset.productId
  const csrfToken = inputElement.dataset.csrf
  const parentItem = inputElement.closest('tr')

  if (value.length === 0 || value <= 0){
    event.target.value = 1
    value = 1
  }

  if (inputValue !== value){
    const result = updateCartItemRequest(productId, value, csrfToken)

    result.then(function(json){
      json.items.forEach(function (item){
        if(productId === item[0])
          parentItem.querySelector('#productSum').innerText = item[1].total_sum.toString()
      })

      updateCartAmount()
    })
  }
}

function saveCurrentInputValue(event){
  inputValue = event.target.value
}

document.addEventListener('DOMContentLoaded', function() {
  const quantityInputs = document.querySelectorAll('.item-quantity')

  quantityInputs.forEach(function(input) {
    input.addEventListener("focus", saveCurrentInputValue)
    input.addEventListener("focusout", updateQuantityItemCart)
  })
})

function applyDiscountCoupon(csrf_token){
  const couponInput = document.querySelector('.section-cart-counting-coupon-input')

  if (couponInput.value.length > 0) {
    const result = applyCouponRequest(couponInput.value, csrf_token)
    result.then(function(json) {
      if (json.status === 'success') {
        couponInput.style.borderColor = DEFAULT_COLOR_BORDER
        document.getElementById('discount').innerHTML = json.discount

        updateCartTotalAmount()
      } else {
        couponInput.style.borderColor = ERROR_COLOR_BORDER
      }
    })
  }else{
    showNotification('error', ERROR_MESSAGE['errorApplyCoupon'])
    couponInput.style.borderColor = ERROR_COLOR_BORDER
  }
}