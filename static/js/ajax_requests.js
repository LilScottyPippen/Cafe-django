function makeAjaxRequest(options) {
    $.ajax({
        type: options.type,
        url: options.url,
        headers: {
            'X-CSRFToken': options.csrf_token
        },
        dataType: 'json',
        success: function(response) {
            showNotification(response.status, response.message)
        },
        error: function(response) {
            showNotification(response.responseJSON.status, response.responseJSON.message)
        }
    });
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