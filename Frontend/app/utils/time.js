export function formatDuration(iso8601Duration) {
  return iso8601Duration.substring(2).toLowerCase()
}

export function formatTime(dateTime) {
  return new Date(dateTime).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  })
}

export function formatPrice(value, currency, location) {
  const userLocale = navigator.language || 'en-US'
  return Intl.NumberFormat(userLocale, {style: 'currency', currency,  currencyDisplay: 'symbol'}).format(value)
}