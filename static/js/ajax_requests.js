function makeAjaxRequest(options) {
    return new Promise(function(resolve, reject) {
        $.ajax({
            type: options.type,
            url: options.url,
            headers: {
                'X-CSRFToken': options.csrf_token
            },
            dataType: 'json',
            success: function (response) {
                resolve(response)
                showNotification(response.status, response.message)
            },
            error: function (response) {
                reject(response)
                showNotification(response.responseJSON.status, response.responseJSON.message)
            }
        })
    })
}

function getCartAmountRequest(){
    return makeAjaxRequest({
        type: "GET",
        url: '/cart/get-amount'
    })
}

function addCartItemRequest(productId, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: `/cart/add/${productId}`,
        csrf_token: csrf_token
    })
}

function deleteCartItemRequest(productId, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: `/cart/delete/${productId}`,
        csrf_token: csrf_token
    })
}

function updateCartItemRequest(productId, quantity, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: `/cart/add/${productId}/${quantity}`,
        csrf_token: csrf_token
    })
}

function applyCouponRequest(coupon, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: `/cart/coupon/${coupon}`,
        csrf_token: csrf_token
    })
}