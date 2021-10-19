import { cloneDeep } from 'lodash';

function processObject(object: Object) {
  const result = object;
  Object.keys(result).forEach(key => {
    if (result[key] === undefined) {
      result[key] = null;
    } else if (result[key] !== null && typeof result[key] === 'object') {
      result[key] = processObject(result[key]);
    }
  });
  return result;
}

export default function replaceUndefinedByNull(object: Object) {
  const copy = cloneDeep(object);
  return processObject(copy);
}
