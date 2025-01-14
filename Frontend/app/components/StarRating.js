import _ from '@/app/styles/StarRating.module.css'

function StarRating({rating}) {
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
  return <div className={_.outer}>
    <div className={_.iconsContainer}>{stars}</div>
    <span className={_.ratingNumber}>{rating}</span>
  </div>;
}

export default StarRating