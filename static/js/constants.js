const DEFAULT_COLOR_BORDER = 'white'
const ERROR_COLOR_BORDER = 'red'

const ERROR_MESSAGES = {
    'errorApplyCoupon': 'Введите купон.',
    'invalidName': 'Введите корректное имя.',
    'invalidPhone': 'Введите номер телефона в формате BY.',
    'invalidMail': 'Введите корректный e-mail.',
    'invalidAddress': 'Введите корректный адрес.'
}

const STRING_REGEX = /^\p{L}{3,}$/u
const ADDRESS_REGEX = /^.{3,}$/u
const PHONE_REGEX = /^(?:\+375|375)\d{9}$/
const MAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/