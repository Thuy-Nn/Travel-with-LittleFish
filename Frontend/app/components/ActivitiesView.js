import _ from '../styles/ActivitiesView.module.css'
import {useState} from 'react'


export default function ActivitiesView({responseContent, max = 5}) {
  // console.log(responseContent)
  if (!responseContent) return null

  // Convert object to array and limit the number of items
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


function StarRating({ rating }) {
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    if (i <= Math.floor(rating)) {
      // Full star
      stars.push(<span key={i} className={_.icon + ' icon-star-full'}/>);
    } else if (i === Math.ceil(rating) && !Number.isInteger(rating)) {
      // Half star (only if rating is not an integer)
      stars.push(<span key={i} className={_.icon + ' icon-star-half'}/>);
    } else {
      // Empty star
      stars.push(<span key={i} className={_.icon + ' icon-star-empty'}/>);
    }
  }
  return <span>{stars}</span>;
}

function ActivitiesItem({name, address, rating, weekday_text, image_url}) {
  const [showOpeningHours, setShowOpeningHours] = useState(false)

  const toggleOpeningHours = () => {
    setShowOpeningHours(!showOpeningHours)
  }


  return <div className={_.ActivitiesItemOuter}>
    <div className={_.ActivitiesItemLeftView}>
      <div className={_.ActivitiesName}>
        <span>{name}</span>
      </div>
      <div className={_.ActivitiesAdress}>
        <span className='icon__left icon-map-pin'/>
        <span>{address}</span>
      </div>
      <div className={_.ActivitiesRating}>
        <StarRating rating={rating}/>
        <span> {rating}</span>
      </div>
      <div className={_.Weekday_text}>
        <button className={_.openingHoursButton} onClick={toggleOpeningHours}>
          <span>Opening Hours</span>
          <span className={_.openingHoursIcon + (showOpeningHours ? ' icon-chevron-up' : ' icon-chevron-down')}/>
        </button>
        {showOpeningHours && weekday_text &&
          weekday_text.map((text, index) => {
            const [day, time] = text.split(": "); // Split into day and time
            return (
              <div key={index} className={_.Weekday_text}>
                <span className={_.Weekday}>{day}: </span>
                <span className={_.Timeday}>{time}</span>
              </div>
            );
          })}
      </div>
    </div>
    <div className={_.ActivitiesItemRightView}>
      <div className={_.thumbnailImg} style={{backgroundImage: `url("${image_url}")`}}/>
    </div>
  </div>
}