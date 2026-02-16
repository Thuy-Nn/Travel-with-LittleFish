import { initializeApp } from "firebase/app"
import {
  collection,
  deleteDoc,
  doc,
  endAt,
  endBefore,
  getDoc,
  getDocs,
  getFirestore,
  limit,
  orderBy,
  query,
  runTransaction,
  setDoc,
  startAfter,
  startAt,
  updateDoc,
  where,
  writeBatch
} from 'firebase/firestore'

const firebaseConfig = {
  apiKey: ,
  authDomain:,
  projectId:,
  storageBucket: ,
  messagingSenderId: ,
  appId: 
};

// Initialize Firebase
const fbApp = initializeApp(firebaseConfig)


// FIRESTORE
export const mainDatabase = getFirestore(fbApp)

export function getFbRef(db, queryDoc) {
  return doc(db, ...queryDoc)
}

export function addNewFbRef(db, queryDoc) {
  return doc(collection(db, ...queryDoc))
}

export async function getFbDoc(db, queryDoc) {
  return await getDoc(doc(db, ...queryDoc))
}

export async function getFbDocWithRef(ref) {
  return await getDoc(ref)
}

export async function getFbDocs(db, queryCol) {
  return await getDocs(collection(db, ...queryCol))
}

export async function setFbDoc(db, queryDoc, data, opt) {
  if (opt) await setDoc(doc(db, ...queryDoc), data, opt)
  else await setDoc(doc(db, ...queryDoc), data)
}

export async function setFbDocWithRef(ref, data, opt) {
  if (opt) await setDoc(ref, data, opt)
  else await setDoc(ref, data)
}

export async function updateFbDoc(db, queryDoc, data) {
  await updateDoc(doc(db, ...queryDoc), data)
}

export async function updateFbDocWithRef(ref, data) {
  await updateDoc(ref, data)
}

export async function deleteFbDoc(db, queryDoc) {
  await deleteDoc(doc(db, ...queryDoc))
}

export async function deleteFbDocWithRef(ref) {
  await deleteDoc(ref)
}

export function getFbWriteBatch(db) {
  return writeBatch(db)
}

export function setFbBatch(batch, db, queryDoc, data, opt) {
  const ref = doc(db, ...queryDoc)
  if (opt) batch.set(ref, data, opt)
  else batch.set(ref, data)
}

export async function runFbTrans(db, func) {
  await runTransaction(db, func)
}

export const QUERY_TYPE = {
  where: 'where',
  orderBy: 'orderBy',
  limit: 'limit',
  startAt: 'startAt',
  startAfter: 'startAfter',
  endAt: 'endAt',
  endBefore: 'endBefore',
}

export async function getFbQuery(db, queryCol, criteria) {
  const ref = collection(db, ...queryCol)

  const conditions = []
  for (let c of criteria) {
    if (c[0] === QUERY_TYPE.where) {
      conditions.push(where(c[1], c[2], c[3]))
    } else if (c[0] === QUERY_TYPE.orderBy) {
      if (c.length > 2) conditions.push(orderBy(c[1], c[2]))
      else conditions.push(orderBy(c[1]))
    } else if (c[0] === QUERY_TYPE.limit) {
      conditions.push(limit(c[1]))
    } else if (c[0] === QUERY_TYPE.startAt) {
      conditions.push(startAt(c[1]))
    } else if (c[0] === QUERY_TYPE.startAfter) {
      conditions.push(startAfter(c[1]))
    } else if (c[0] === QUERY_TYPE.endAt) {
      conditions.push(endAt(c[1]))
    } else if (c[0] === QUERY_TYPE.endBefore) {
      conditions.push(endBefore(c[1]))
    }
  }

  const q = query(ref, ...conditions)
  return await getDocs(q)
}
