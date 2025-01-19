import exchange from '@/app/const/exchange.json'


export function formatPrice(value, currency, targetCurrency = 'EUR') {

  let displayedValue = value

  // convert the currency if needed
  if (currency !== targetCurrency) {
    const srcRate = exchange.rates[currency.toUpperCase()]
    const dstRate = exchange.rates[targetCurrency.toUpperCase()]
    displayedValue = value * dstRate / srcRate
  }

  const userLocale = navigator.language || 'en-US'
  return Intl.NumberFormat(userLocale, {
    style: 'currency',
    currency: targetCurrency,
    currencyDisplay: 'symbol'
  }).format(displayedValue)
}

export function convertPrice(value, sourceCurrency, targetCurrency = 'EUR') {
  if (sourceCurrency === targetCurrency) return value
  const srcRate = exchange.rates[sourceCurrency.toUpperCase()]
  const dstRate = exchange.rates[targetCurrency.toUpperCase()]
  return value * dstRate / srcRate
}