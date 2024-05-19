function makeAjaxRequest(options) {
    return new Promise(function(resolve, reject) {
        $.ajax({
            type: options.type,
            url: options.url,
            contentType: 'application/json',
            data: JSON.stringify(options.data),
            headers: {
                'X-CSRFToken': options.csrf_token
            },
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
        url: '/cart/add',
        data: {
            product_id: productId
        },
        csrf_token: csrf_token
    })
}

function deleteCartItemRequest(productId, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: '/cart/delete',
        data: {
            product_id: productId
        },
        csrf_token: csrf_token
    })
}

function updateCartItemRequest(productId, quantity, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: '/cart/add',
        data: {
            product_id: productId,
            quantity: quantity
        },
        csrf_token: csrf_token
    })
}

function applyCouponRequest(code, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: '/cart/coupon',
        data: {
            code: code
        },
        csrf_token: csrf_token
    })
}

function createOrderRequest(client_data, csrf_token){
    return makeAjaxRequest({
        type: "POST",
        url: '/create-order',
        data: {
            client_data: client_data
        },
        csrf_token: csrf_token
    })
}