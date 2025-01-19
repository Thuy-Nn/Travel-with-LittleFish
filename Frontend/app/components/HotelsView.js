import _ from '../styles/HotelsView.module.css'
import StarRating from '@/app/components/StarRating'
import {formatPrice} from '@/app/utils/price'

export default function HotelsView({responseType, responseContent, max = 10, favoriteIds, toggleFavorite}) {
  if (!responseContent) return null

  const displayedData = responseContent.slice(0, max)
  // console.log(displayedData)

  if (displayedData.length === 0) {
    return <span>No results found</span>
  }

  return <div>
    {displayedData.map((item, index) =>
      <HotelItem key={'hotels-' + index}
                 item={item}
                 itemType={responseType}
                 isFavorite={favoriteIds.includes(responseType + '__' + item['id'])}
                 toggleFavorite={toggleFavorite}
      />)}
  </div>
}

export function HotelItem({item, itemType, isFavorite, toggleFavorite}) {
  const {id, name, distance, offer, overallRating, numberOfRatings, image} = item

  const _toggleFavorite = () => {
    if (!toggleFavorite) return
    toggleFavorite(itemType, id, item)
  }

  return <div className={_.hotelsItemOuter + ' item-outer'}>
    <div className={_.hotelsItemLeftView}>
      <div className={_.hotelName}>{name}</div>
      {distance && <div className={_.hotelDistance}>{distance.value} km from downtown</div>}
      <div className={_.hotelDescription}>{offer.room.description.text}</div>

      {overallRating && <div className={_.hotelRating}>
        <StarRating rating={(overallRating / 20).toFixed(1)}/>
        <span className={_.numberOfRatings}>({numberOfRatings.toLocaleString()} Reviews)</span>
      </div>}

      <div className={_.hotelPrice}>{formatPrice(offer.price.total, offer.price.currency)}</div>
    </div>
    <div className={_.hotelsItemRightView}>
      <div className={_.thumbnailPlaceholder}>
        <span className={_.thumbnailPlaceholderIcon + ' icon-image'}/>
      </div>
      <div className={_.thumbnailImg} style={{backgroundImage: `url("${image}")`}}/>
    </div>
    <button className={isFavorite ? 'favorite-icon__marked icon-heart' : 'favorite-icon icon-heart-o'}
            onClick={_toggleFavorite}/>
  </div>
}