'use client'

import _ from './Home.module.css'
import {useState} from 'react'
import {CONTENT_TYPE} from '@/app/const/CONTENT_TYPE'
import FlightView from '@/app/components/FlightsView'
import ActivitiesView from '@/app/components/ActivitiesView'
import HotelsView from '@/app/components/HotelsView'
import {CONFIG} from '@/app/const/CONFIG'


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

  const toggleSidebar = () => {
    setShowSidebar(!showSidebar)
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

    if (data.type === CONTENT_TYPE.text) {
      return <span>{typeof data.content === 'string' ? data.content : JSON.stringify(data.content)}</span>
    }
    if (data.type === CONTENT_TYPE.flights) {
      return <FlightView responseContent={data.content}/>
    }
    if (data.type === CONTENT_TYPE.hotels) {
      return <HotelsView responseContent={data.content}/>
    }
    if (data.type === CONTENT_TYPE.activities) {
      return <ActivitiesView responseContent={data.content}/>
    }
  }

  return (
    <div className={_.travelPage}>
      <div className={_.headerContainer}>
        <img src="favicon.ico" className={_.headerIcon}/>
        <span className={_.headerTitle}>Little Fish</span>
        <div className={_.toolbarContainer}>
          <button className={_.toolbarButton + ' icon-heart'} onClick={toggleSidebar}/>
        </div>
      </div>
      <div className={_.mainContent}>
        <div className={_.chatContainer}>
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
        <div className={_.inputContainer}>
          {/*form submit he thong mac dinh kem an enter*/}
          <form onSubmit={sendMessage}>
            {/*placeholder: chu chim ben duoi*/}
            <input className={_.messageTextbox} placeholder='Enter your prompt here'
                   value={inputMessage} onChange={inputMessageHandler}/>
            <button className={_.sendButton + ' icon-arrow-up-circle'} type='submit' disabled={!inputMessage}/>
          </form>
        </div>
      </div>
      <div className={showSidebar ? _.sidebarContainer : _.sidebarContainer__collapsed}>
        <button className={_.toolbarButton + ' icon-x'} onClick={toggleSidebar}/>
      </div>
    </div>
  );
}
