import _ from '../styles/FlightView.module.css'
import {formatDuration, formatPrice, formatTime} from '@/app/utils/time'
import {formatAirport} from '@/app/utils/airport'


export default function FlightView({responseContent, max = 10}) {
  if (!responseContent) return null

  /*
  * const data = responseContent['data']
  * const dictionaries = responseContent['dictionaries']
  */
  const {data, dictionaries} = responseContent
  const displayedData = data.slice(0, max) // slice: extract max elements starting from 0

  return <div>
    {displayedData.map(item => <FlightItem key={'flight-' + item['id']}
                                           id={item['id']}
                                           itineraries={item['itineraries']}
                                           price={item['price']}
    dictionaries={dictionaries} />)}
  </div>
}

function FlightItem({id, itineraries, price, dictionaries}) {
  return <div className={_.flightItemOuter}>
    <div className={_.flightItemLeftView}>
      {itineraries.map((itiner, i) => <div key={'itiner-' + i}>
        <div className={_.flightTotalDuration}>
          <span className={_.flightTotalDurationText}>Total Duration:</span>
          <span>{formatDuration(itiner.duration)}</span>
        </div>
        {itiner.segments.map((seg, j) => <div key={'seg-' + j} className={_.flightDetails}>
            <div className={_.flightCarrier}>
              {/*<div className={_.flightCarrierCode}>{seg.carrierCode}</div>*/}
              <img className={_.flightCarrierLogo} title={dictionaries['carriers'][seg.carrierCode]}
                   src={`https://content.r9cdn.net/rimg/provider-logos/airlines/v/${seg.carrierCode}.png`}/>
              {/*<div className={_.flightCarrierName}>{dictionaries['carriers'][seg.carrierCode]}</div>*/}
            </div>
            <div className={_.flightTime}>
              <div className={_.flightTimeHour}>{formatTime(seg.departure.at)} - {formatTime(seg.arrival.at)}</div>
              <div className={_.flightPlace}>
                <span title={formatAirport(seg.departure.iataCode)}>{seg.departure.iataCode}</span>
                <span className={_.flightIcon + ' icon-airplane'}/>
                <span title={formatAirport(seg.arrival.iataCode)}>{seg.arrival.iataCode}</span>
              </div>
            </div>
            <div className={_.flightDuration}>{formatDuration(seg.duration)}</div>
        </div>)}
      </div>)}
    </div>
    <div className={_.flightItemRightView}>
      <span className={_.flightPrice}>{formatPrice(price.total, price.currency)}</span>
    </div>
  </div>
}