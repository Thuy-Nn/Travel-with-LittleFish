'use client'

import _ from './Home.module.css'
import {useState, useEffect, useRef} from 'react'
import {CONTENT_TYPE} from '@/app/const/CONTENT_TYPE'
import FlightView from '@/app/components/FlightsView'
import ActivitiesView from '@/app/components/ActivitiesView'
import HotelsView from '@/app/components/HotelsView'


export default function Home() {
  // useState: web hien thi len
  // const khac var/let: var/let thay doi dc value, con const gia tri khong thay doi
  // trong truong hop nay list khong doi nhung item statusMessage van thay doi binh thuong
  // kien thuc cho thay
  // nen dung "const" thay vi "let", khong dung "var"
  const [statusMessage, setStatusMessage] = useState('(empty message)')
  const [historyItems, setHistoryItems] = useState(null)
  const [inputMessage, setInputMessage] = useState('')
  const [chatMessages, setChatMessages] = useState([])
  const [processing, setProcessing] = useState(false)

  // useRef: luu gia tri co dinh sau moi lan render
  const _socketConnection = useRef(null)

  // useEffect: ham load websocket run voi dieu kien trong [] --> khi [] rong thi chi chay 1 lan
  useEffect(() => {
    _socketConnection.current = new WebSocket('ws://localhost:8009')
    // addEventListener theo doi
    _socketConnection.current.addEventListener('open', () => {
      console.log('WebSocket connection opened')
    })
    _socketConnection.current.addEventListener('error', e => {
      console.log('Connection Error:', e)
    })
    _socketConnection.current.addEventListener('message', receiveMessage)

    receiveMessage()

  }, [])

  const favoriteHandler = () => {
    setStatusMessage('User clicked favorite!')
  }

  const settingsHandler = () => {
    setStatusMessage('User clicked settings!')
  }

  const userHandler = () => {
    setStatusMessage('User clicked profile!')
  }

  const inputMessageHandler = e => {
    setInputMessage(e.target.value)
  }

  const sendMessage = e => {
    // tranh refresh lai trang khi submit form
    e.preventDefault()

    if (!inputMessage) return

    /*
    * newChatMessages = [...chatMessages]
    * newChatMessages.push({
    *   'role': 'user',
    *   'content': inputMessage
    * })
    * setChatMessages(chatMessages)
    * */

    setChatMessages(currentMessages => [...currentMessages, {
      'role': 'user',
      'data': {
        type: 'text',
        content: inputMessage
      }
    }])
    setInputMessage('')

    // send inputMessage to server
    _socketConnection.current.send(inputMessage)
    setProcessing(true)
  }

  const receiveMessage = e => {
    // console.log('Received Message:', e)
    if (!e) return
    if (!e.data) return

    const responseData = JSON.parse(e.data)
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
      return <span>{data.content}</span>
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
      <div className={_.leftSidebar}>
        <div className={_.headerContainer}>
          <img src="favicon.ico" className={_.headerIcon}/>
          <span className={_.headerTitle}>Little Fish</span>
        </div>
        <div className={_.historyContainer}>
          {historyItems ?
            historyItems.map((item, index) => <div key={index} className={_.historyItem}>
              <span>{item}</span>
            </div>)
            : null}
        </div>
      </div>
      <div className={_.mainContent}>
        {/*<div className={_.toolbarPanel}>*/}
        {/*  <span>Status: {statusMessage}</span>*/}
        {/*  <div className={_.toolbarIconContainer}>*/}
        {/*    <button className={_.toolbarIcon + ' icon-heart'} onClick={favoriteHandler}/>*/}
        {/*    <button className={_.toolbarIcon + ' icon-settings'} onClick={settingsHandler}/>*/}
        {/*    <button className={_.toolbarIcon + ' icon-user'} onClick={userHandler}/>*/}
        {/*  </div>*/}
        {/*</div>*/}
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
    </div>
  );
}
