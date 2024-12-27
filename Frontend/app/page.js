'use client'

import _ from './Home.module.css'
import {useState, useEffect, useRef} from 'react'


export default function Home() {
  // useState: web hien thi len
  // const khac var/let: var/let thay doi dc value, con const gia tri khong thay doi
  // trong truong hop nay list khong doi nhung item statusMessage van thay doi binh thuong
  // kien thuc cho thay
  // nen dung "const" thay vi "let", khong dung "var"
  const [statusMessage, setStatusMessage] = useState('(empty message)')
  const [historyItems, setHistoryItems] = useState([
    "hehe", "duongxaugai", "thuyxinhgai"
  ])
  const [inputMessage, setInputMessage] = useState('When will I be married?')

  // useRef: luu gia tri co dinh sau moi lan render
  const _socketConnection = useRef(null)

  // useEffect: ham load websocket run voi dieu kien trong [] --> khi [] rong thi chi chay 1 lan
  useEffect(() => {
    _socketConnection.current = new WebSocket('ws://localhost:8003')
    // addEventListener theo doi
    _socketConnection.current.addEventListener('message', receiveMessage)
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

    // send inputMessage to server
    _socketConnection.current.send(inputMessage)
  }

  const receiveMessage = e => {

  }

  return (
    <div className={_.travelPage}>
      <div className={_.leftSidebar}>
        <div className={_.headerContainer}>
          <img src="favicon.ico" className={_.headerIcon}/>
          <span className={_.headerTitle}>Little Fish</span>
        </div>
        <div className={_.historyContainer}>
          {historyItems.map((item, index) => <div key={index} className={_.historyItem}>
            <span>{item}</span>
          </div>)}
        </div>
      </div>
      <div className={_.mainContent}>
        <div className={_.toolbarPanel}>
          <span>Status: {statusMessage}</span>
          <div className={_.toolbarIconContainer}>
            <button className={_.toolbarIcon + ' icon-heart'} onClick={favoriteHandler}/>
            <button className={_.toolbarIcon + ' icon-settings'} onClick={settingsHandler}/>
            <button className={_.toolbarIcon + ' icon-user'} onClick={userHandler}/>
          </div>
        </div>
        <div className={_.chatContainer}>
          <div className={_.chatPanel}></div>
        </div>
        <div className={_.inputContainer}>
          {/*form submit he thong mac dinh kem an enter*/}
          <form onSubmit={sendMessage}>
            {/*placeholder: chu chim ben duoi*/}
            <input className={_.messageTextbox} placeholder='Enter your prompt here'
                   value={inputMessage} onChange={inputMessageHandler}/>
            <button className={_.sendButton + ' icon-arrow-up-circle'} type='submit'/>
          </form>
        </div>
      </div>
    </div>
  );
}
