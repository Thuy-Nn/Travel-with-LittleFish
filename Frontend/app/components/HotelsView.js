import _ from '../styles/HotelsView.module.css'
import StarRating from '@/app/components/StarRating'

export default function HotelsView({responseContent, max = 10}) {
  if (!responseContent) return null

  const dataArr = Object.values(responseContent).filter((item) => typeof item === "object")
  const data = dataArr.slice(0, max)
  // console.log(data)

  return <div>
    {data.map((item, index) => <HotelItem key={'hotels-' + index}
                                          name={item.name}
                                          geoCode={item.geoCode}
                                          distance={item.distance}
                                          offer={item.offer}
                                          overallRating={item.overallRating}
                                          numberOfRatings={item.numberOfRatings}
                                          image={item.image}
    />)}
  </div>
}

function HotelItem({name, geoCode, distance, offer, overallRating, numberOfRatings, image}) {
  return <div className={_.hotelsItemOuter}>
    <div className={_.hotelsItemLeftView}>
      <div className={_.hotelName}>{name}</div>
      {distance && <div className={_.hotelDistance}>{distance.value} km from downtown</div>}
      <div className={_.hotelDescription}>{offer.room.description.text}</div>
      <div className={_.hotelRating}>
        <StarRating rating={overallRating / 20}/>
        <span className={_.overallRating}>{(overallRating / 20).toFixed(1)}</span>
        <span className={_.numberOfRatings}> {numberOfRatings} Reviews</span>
      </div>
      <div className={_.hotelPrice}>{`${offer.price.total} ${offer.price.currency}`}</div>
    </div>
    <div className={_.hotelsItemRightView}>
      <div className={_.thumbnailImg} style={{backgroundImage: `url("${image}")`}}/>
    </div>
  </div>
}