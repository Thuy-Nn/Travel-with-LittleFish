import _ from '../styles/FlightView.module.css'
import {formatDuration, formatTime} from '@/app/utils/time'
import {formatPrice} from '@/app/utils/price'
import {formatAirport} from '@/app/utils/airport'


export default function FlightView({responseType, responseContent, max = 10, favoriteIds, toggleFavorite}) {
  if (!responseContent) return null

  // console.log(responseContent)

  /*
  * const data = responseContent['data']
  * const dictionaries = responseContent['dictionaries']
  */
  const {data, dictionaries} = responseContent
  const displayedData = data.slice(0, max) // slice: extract max elements starting from 0

  if (displayedData.length === 0) {
    return <span>No results found</span>
  }

  for (let d of displayedData) {
    for (let itiner of d['itineraries']) {
      for (let seg of itiner['segments']) {
        seg['carrierName'] = dictionaries['carriers'][seg.carrierCode]
      }
    }
  }

  return <div>
    {displayedData.map(item =>
      <FlightItem key={'flight-' + item['id']}
                  item={item}
                  itemType={responseType}
                  isFavorite={favoriteIds.includes(responseType + '__' + item['id'])}
                  toggleFavorite={toggleFavorite}
      />)}
  </div>
}

export function FlightItem({item, itemType, isFavorite, toggleFavorite}) {
  const {id, itineraries, price} = item

  const _toggleFavorite = () => {
    if (!toggleFavorite) return
    toggleFavorite(itemType, id, item)
  }

  return <div className={_.flightItemOuter + ' item-outer'}>
    <div className={_.flightItemLeftView}>
      {itineraries.map((itiner, i) => <div key={'itiner-' + i} className={_.flightItemItineraryView}>
        <div className={_.flightTotalDuration}>
          <span className={_.flightTotalDurationText}>Total Duration:</span>
          <span>{formatDuration(itiner.duration)}</span>
        </div>
        {itiner.segments.map((seg, j) => <div key={'seg-' + j} className={_.flightDetails}>
          <div className={_.flightCarrier}>
            {/*<div className={_.flightCarrierCode}>{seg.carrierCode}</div>*/}
            <img className={_.flightCarrierLogo} title={seg['carrierName']}
                 src={`https://content.r9cdn.net/rimg/provider-logos/airlines/v/${seg['carrierCode']}.png`}/>
          </div>
          <div className={_.flightTime}>
            <div
              className={_.flightTimeHour}>{formatTime(seg['departure']['at'])} - {formatTime(seg['arrival']['at'])}</div>
            <div className={_.flightPlace}>
              <span title={formatAirport(seg['departure']['iataCode'])}>{seg['departure']['iataCode']}</span>
              <span className={_.flightIcon + ' icon-airplane'}/>
              <span title={formatAirport(seg['arrival']['iataCode'])}>{seg['arrival']['iataCode']}</span>
            </div>
          </div>
          <div className={_.flightDuration}>{formatDuration(seg.duration)}</div>
        </div>)}
      </div>)}
    </div>
    <div className={_.flightItemRightView}>
      <span className={_.flightPrice}>{formatPrice(price.grandTotal, price.currency)}</span>
    </div>
    <button className={isFavorite ? 'favorite-icon__marked icon-heart' : 'favorite-icon icon-heart-o'}
            onClick={_toggleFavorite}/>
  </div>
}
