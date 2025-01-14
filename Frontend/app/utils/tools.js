export function findItemInArray(array, key, value, valueTransformFunc) {
  let foundItem = null
  let index = -1
  for (let i = 0; i < array.length; i++) {
    let v = array[i][key]
    if (valueTransformFunc) v = valueTransformFunc(v)
    if (v === value) {
      foundItem = array[i]
      index = i
      break
    }
  }

  return {
    item: foundItem,
    index: index
  }
}