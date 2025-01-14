import _ from '../styles/ActivitiesView.module.css'
import {useState} from 'react'
import StarRating from '@/app/components/StarRating'


export default function ActivitiesView({responseType, responseContent, max = 10, favoriteIds, toggleFavorite}) {
  // console.log(responseContent)
  if (!responseContent) return null

  // Convert object to array
  const displayedData = responseContent.slice(0, max)
  // console.log(displayedData)

  if (displayedData.length === 0) {
    return <span>No results found</span>
  }

  return <div>
    {displayedData.map((item, index) =>
      <ActivitiesItem key={'activities-' + index} // index them so thu tu
                      item={item}
                      itemType={responseType}
                      isFavorite={favoriteIds.includes(responseType + '__' + item['id'])}
                      toggleFavorite={toggleFavorite}
      />)}
  </div>
}

export function ActivitiesItem({item, itemType, isFavorite, toggleFavorite}) {
  const {id, name, address, rating, weekday_text, images} = item
  const [showOpeningHours, setShowOpeningHours] = useState(false)

  const toggleOpeningHours = () => {
    setShowOpeningHours(!showOpeningHours)
  }

  const _toggleFavorite = () => {
    if (!toggleFavorite) return
    toggleFavorite(itemType, id, item)
  }

  return <div className={_.activitiesItemOuter + ' item-outer'}>
    <div className={_.activitiesItemLeftView}>
      <div className={_.activitiesName}>
        <span>{name}</span>
      </div>
      <div className={_.activitiesAddress}>
        <span className='icon__left icon-map-pin'/>
        <span>{address}</span>
      </div>
      {rating && <div className={_.activitiesRating}>
        <StarRating rating={rating}/>
      </div>}
      <div className={_.weekday_text}>
        <button className={_.openingHoursButton} onClick={toggleOpeningHours}>
          <span>Opening Hours</span>
          <span className={_.openingHoursIcon + (showOpeningHours ? ' icon-chevron-up' : ' icon-chevron-down')}/>
        </button>
        {showOpeningHours && weekday_text &&
          weekday_text.map((text, index) => {
            const [day, time] = text.split(": "); // Split into day and time
            return (
              <div key={index} className={_.weekday_text}>
                <span className={_.weekday}>{day}: </span>
                <span className={_.timeday}>{time}</span>
              </div>
            );
          })}
      </div>
    </div>
    <div className={_.activitiesItemRightView}>
      <div className={_.thumbnailImg} style={{backgroundImage: `url("${images}")`}}/>
    </div>
    <button className={isFavorite ? 'favorite-icon__marked icon-heart' : 'favorite-icon icon-heart-o'}
            onClick={_toggleFavorite}/>
  </div>
}