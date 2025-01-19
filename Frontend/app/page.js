'use client'

import _ from './Home.module.css'
import {useEffect, useRef, useState} from 'react'
import {CONTENT_TYPE} from '@/app/const/CONTENT_TYPE'
import FlightView, {FlightItem} from '@/app/components/FlightsView'
import ActivitiesView, {ActivitiesItem} from '@/app/components/ActivitiesView'
import HotelsView, {HotelItem} from '@/app/components/HotelsView'
import {CONFIG} from '@/app/const/CONFIG'
import {deleteFbDoc, getFbDocs, mainDatabase, setFbDoc} from '@/app/fb'
// import responseData from '@/app/data/analyze.json'

import {findItemInArray} from '@/app/utils/tools'
import {formatPrice, convertPrice} from '@/app/utils/price'


export default function Home() {
  // useState: web hien thi len
  // const khac var/let: var/let thay doi dc value, con const gia tri khong thay doi
  // trong truong hop nay list khong doi nhung item statusMessage van thay doi binh thuong
  // kien thuc cho thay
  // nen dung "const" thay vi "let", khong dung "var"
  const [inputMessage, setInputMessage] = useState('')
  const [chatMessages, setChatMessages] = useState([])
  const [processing, setProcessing] = useState(false)
  const [showSidebar, setShowSidebar] = useState(false)

  const [favoriteItems, setFavoriteItems] = useState([])

  const chatViewRef = useRef(null)

  useEffect(() => {
    loadFavorites()
      .then(setFavoriteItems)
      .catch(console.log)

    // setChatMessages(currentMessages => [...currentMessages, {
    //   'role': 'server',
    //   'data': responseData
    // }])
  }, [])

  useEffect(() => {
    scrollToTop()
  }, [chatMessages.length])

  const toggleSidebar = () => {
    setShowSidebar(!showSidebar)
  }

  const toggleFavorite = async (type, id, item) => {
    const favId = type + '__' + id
    const foundItem = findItemInArray(favoriteItems, 'favId', favId)
    if (foundItem.item) {
      await removeFavorite(favId)
      setFavoriteItems([...favoriteItems.toSpliced(foundItem.index, 1)])

    } else {
      item['favId'] = favId
      item['type'] = type
      item['favorited_at'] = new Date().toISOString()
      await addFavorite(favId, item)
      setFavoriteItems([...favoriteItems, item])
    }
  }

  const scrollToTop = () => {
    if (chatViewRef.current) {
      chatViewRef.current.scrollTop = chatViewRef.current.scrollHeight
    }
  }

  const inputMessageHandler = e => {
    setInputMessage(e.target.value)
  }

  const sendMessage = async e => {
    // tranh refresh lai trang khi submit form
    e.preventDefault()

    if (!inputMessage) return

    setChatMessages(currentMessages => [...currentMessages, {
      'role': 'user',
      'data': {
        type: 'text',
        content: inputMessage
      }
    }])
    setInputMessage('')

    setProcessing(true)

    const response = await fetch(CONFIG.SERVER_ROOT_API + 'chat', {
      method: 'POST',
      body: JSON.stringify({
        message: inputMessage,
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })

    const responseData = await response.json()
    console.log(responseData)

    setChatMessages(currentMessages => [...currentMessages, {
      'role': 'server',
      'data': responseData
    }])
    setProcessing(false)
  }

  const renderContent = data => {
    if (!data) return null
    if (!data.content) return null

    if (data.content['errors']) {
      return <span>Sorry, I don't understand.</span>
    }

    const favoriteIds = favoriteItems.map(item => item['favId'])

    if (data.type === CONTENT_TYPE.error) {
      console.log(data.content)
      return <span>Something wrong happened</span>
    }
    if (data.type === CONTENT_TYPE.text) {
      return <span>{typeof data.content === 'string' ? data.content : JSON.stringify(data.content)}</span>
    }
    if (data.type === CONTENT_TYPE.flights) {
      return <FlightView responseType={data.type} responseContent={data.content}
                         favoriteIds={favoriteIds} toggleFavorite={toggleFavorite}/>
    }
    if (data.type === CONTENT_TYPE.hotels) {
      return <HotelsView responseType={data.type} responseContent={data.content}
                         favoriteIds={favoriteIds} toggleFavorite={toggleFavorite}/>
    }
    if (data.type === CONTENT_TYPE.attractions || data.type === CONTENT_TYPE.restaurants) {
      return <ActivitiesView responseType={data.type} responseContent={data.content}
                             favoriteIds={favoriteIds} toggleFavorite={toggleFavorite}/>
    }
  }

  const renderFavoriteItem = data => {
    if (data['type'] === CONTENT_TYPE.flights) {
      return <FlightItem key={data['id']} item={data} itemType={data['type']} isFavorite={true}
                         toggleFavorite={toggleFavorite}/>
    } else if (data['type'] === CONTENT_TYPE.hotels) {
      return <HotelItem key={data['id']} item={data} itemType={data['type']}
                        isFavorite={true} toggleFavorite={toggleFavorite}/>
    } else if (data['type'] === CONTENT_TYPE.attractions || data['type'] === CONTENT_TYPE.restaurants) {
      return <ActivitiesItem key={data['id']} item={data} itemType={data['type']}
                             isFavorite={true} toggleFavorite={toggleFavorite}/>
    }
  }

  const calculateTotalPrice = () => {
    let total = 0
    const currency = 'EUR'

    for (let f of favoriteItems) {
      if (f['type'] === 'flights') {
        total += convertPrice(parseFloat(f['price']['grandTotal']), f['price']['currency'])
      } else if (f['type'] === 'hotels') {
        total += convertPrice(parseFloat(f['offer']['price']['total']), f['offer']['price']['currency'])
      }
    }

    return formatPrice(total, currency)
  }

  return (
    <div className={_.travelPage}>
      <div className={_.mainContent}>
        <div className={_.chatContainer} ref={chatViewRef}>
          {chatMessages ? chatMessages.map((item, index) =>
            <div key={index}
                 className={_.chatItem + ' ' + (item.role === 'user' ? _.chatItem__user : _.chatItem__server)}>
              {item.role === 'server' ? <img src="favicon.ico" className={_.chatIcon}/> : null}
              <div className={_.chatItemInner}>
                {renderContent(item.data)}
              </div>
            </div>) : null}
          {processing && <div className={_.chatItem + ' ' + _.chatItem__server}>
            <img src="favicon.ico" className={_.chatIcon}/>
            <img src="loading.gif" className={_.processingGif}/>
          </div>}
        </div>
        <div className={chatMessages.length === 0 ? _.inputContainer__float : _.inputContainer}>
          {/*form submit he thong mac dinh kem an enter*/}
          <form onSubmit={sendMessage}>
            {/*placeholder: chu chim ben duoi*/}
            {chatMessages.length === 0 ? <div className={_.messageTitle}>What can I help with?</div> : null}
            <input className={_.messageTextbox} placeholder='Enter your prompt here'
                   value={inputMessage} onChange={inputMessageHandler}/>
            <button className={_.sendButton + ' icon-arrow-up-circle'} type='submit' disabled={!inputMessage}/>
          </form>
        </div>
      </div>
      <div className={_.headerContainer}>
        <img src="favicon.ico" className={_.headerIcon}/>
        <span className={_.headerTitle}>Little Fish</span>
        <div className={_.toolbarContainer}>
          <button className={_.toolbarButton} onClick={toggleSidebar}>
            <span className='icon-heart'/>
            {favoriteItems.length > 0 ? <span className={_.favoriteNumText}>{favoriteItems.length}</span> : null}
          </button>
        </div>
      </div>
      <div className={showSidebar ? _.sidebarContainer : _.sidebarContainer__collapsed}>
        <div className={_.favoritesContainer}>
          {(!favoriteItems || favoriteItems.length === 0) ?
            <div className='empty-view'>
              <div className='empty-title'>No Favorites Yet</div>
              <div className='empty-message'>Click <span className='icon-heart'/> button to add a favorite.</div>
            </div>
            :
            favoriteItems.map(renderFavoriteItem)
          }
        </div>
        <div className={_.totalPriceContainer}>
          <button className={_.sidebarCloseButton + ' icon-x'} onClick={toggleSidebar}/>
          <span className={_.totalPriceText}>Total Price:</span>
          <span className={_.totalPrice}>{calculateTotalPrice()}</span>
        </div>
      </div>
    </div>
  );
}


async function loadFavorites() {
  const res = await getFbDocs(mainDatabase, [CONFIG.FAVORITES_COL])
  const favorites = []
  res.forEach(r => {
    favorites.push(r.data())
  })
  return favorites.sort((a, b) => {
    const dateA = new Date(a['favorited_at'])
    const dateB = new Date(b['favorited_at'])
    if (dateA < dateB) return -1
    if (dateA > dateB) return 1
    return 0
  })
}

async function addFavorite(favId, item) {
  await setFbDoc(mainDatabase, [CONFIG.FAVORITES_COL, favId], item)
}

async function removeFavorite(favId) {
  await deleteFbDoc(mainDatabase, [CONFIG.FAVORITES_COL, favId])
}