function createOrder(csrf_token){
    const clientData = {
        client_name: document.getElementById('client-name'),
        client_phone: document.getElementById('client-phone'),
        client_mail: document.getElementById('client-mail'),
        client_address: document.getElementById('client-address')
    }

    if(isValidOrder(clientData)){
        const clientDataValue = {}

        for(const key in clientData){
            clientDataValue[key] = clientData[key].value
        }

        const result = createOrderRequest(clientDataValue, csrf_token)

        result.then(function(json){
            if (json.status === 'success')
              setEmptyCart()
        })
    }
}

function isValidOrder(clientData){
    let validOrder = true

    const listRegex = {
        name: STRING_REGEX,
        phone: PHONE_REGEX,
        mail: MAIL_REGEX,
        address: ADDRESS_REGEX
    }

    const listError = {
        name: ERROR_MESSAGES['invalidName'],
        phone: ERROR_MESSAGES['invalidPhone'],
        mail: ERROR_MESSAGES['invalidMail'],
        address: ERROR_MESSAGES['invalidAddress']
    }

    for(const key in clientData){
        const name = clientData[key].name
        const value = clientData[key].value

        if(name in listRegex){
            if(listRegex[name].test(value)){
                clientData[key].style.borderColor = DEFAULT_COLOR_BORDER
            }else{
                validOrder = false
                clientData[key].style.borderColor = ERROR_COLOR_BORDER
                if(name in listError){
                    showNotification('error', listError[name])
                }
            }
        }
    }

    return validOrder
}