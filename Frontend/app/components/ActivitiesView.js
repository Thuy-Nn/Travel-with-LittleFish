import _ from '../styles/ActivitiesView.module.css'
import {useState} from 'react'
import StarRating from '@/app/components/StarRating'


export default function ActivitiesView({responseContent, max = 10}) {
  // console.log(responseContent)
  if (!responseContent) return null

  // Convert object to array
  const activitiesArray = Object.values(responseContent).filter((item) => typeof item === "object")
  // console.log(activitiesArray)

  return <div>
    {activitiesArray.map((item, index) =>
      <ActivitiesItem key={'activities-' + index} // index them so thu tu
                      name={item.name}
                      address={item.address}
                      rating={item.rating}
                      weekday_text={item.weekday_text}
                      image_url={item.images}
      />)}
  </div>
}

function ActivitiesItem({name, address, rating, weekday_text, image_url}) {
  const [showOpeningHours, setShowOpeningHours] = useState(false)

  const toggleOpeningHours = () => {
    setShowOpeningHours(!showOpeningHours)
  }


  return <div className={_.activitiesItemOuter}>
    <div className={_.activitiesItemLeftView}>
      <div className={_.activitiesName}>
        <span>{name}</span>
      </div>
      <div className={_.activitiesAddress}>
        <span className='icon__left icon-map-pin'/>
        <span>{address}</span>
      </div>
      <div className={_.activitiesRating}>
        <StarRating rating={rating}/>
        <span> {rating}</span>
      </div>
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
      <div className={_.thumbnailImg} style={{backgroundImage: `url("${image_url}")`}}/>
    </div>
  </div>
}