import airports from '@/app/const/airports.json'


export function formatAirport(airportCode) {
  if (!airports[airportCode]) return airportCode
  return airports[airportCode]['name']
}