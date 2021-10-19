import shortid from 'shortid';
import { compose } from 'redux';
import persistState, { StorageAdapter } from 'redux-localstorage';
import { isEqual, omitBy, isUndefined } from 'lodash';

/**
 * 使用指定对象添加替换到指定状态对象中指定 arrKey 处的对象。
 *
 * @param state 状态对象。
 * @param arrKey 要添加或替换对象的键。
 * @param obj 要添加或替换的对象。
 */
export function addToObject(
  state: Record<string, any>,
  arrKey: string,
  obj: Record<string, any>,
) {
  const newObject = { ...state[arrKey] };
  const copiedObject = { ...obj };

  if (!copiedObject.id) {
    copiedObject.id = shortid.generate();
  }
  newObject[copiedObject.id] = copiedObject;
  return { ...state, [arrKey]: newObject };
}

/**
 * 使用指定对象更新到指定状态对象中指定 arrKey 处的对象。
 *
 * @param state 状态对象。
 * @param arrKey 要添加或替换对象的键。
 * @param obj 要更新的对象。
 * @param alterations 更新对象。
 */
export function alterInObject(
  state: Record<string, any>,
  arrKey: string,
  obj: Record<string, any>,
  alterations: Record<string, any>,
) {
  const newObject = { ...state[arrKey] };
  newObject[obj.id] = { ...newObject[obj.id], ...alterations };
  return { ...state, [arrKey]: newObject };
}

/**
 * 在数组中更新。
 *
 * @param state 状态对象。
 * @param arrKey
 * @param obj
 * @param alterations
 * @param idKey
 */
export function alterInArr(
  state: Record<string, any>,
  arrKey: string,
  obj: Record<string, any>,
  alterations: Record<string, any>,
  idKey = 'id',
) {
  // Finds an item in an array in the state and replaces it with a
  // new object with an altered property
  const newArr: unknown[] = [];
  state[arrKey].forEach((arrItem: Record<string, any>) => {
    if (obj[idKey] === arrItem[idKey]) {
      newArr.push({ ...arrItem, ...alterations });
    } else {
      newArr.push(arrItem);
    }
  });
  return { ...state, [arrKey]: newArr };
}

/**
 * 依据数组移除。
 *
 * @param state
 * @param arrKey
 * @param obj
 * @param idKey
 */
export function removeFromArr(
  state: Record<string, any>,
  arrKey: string,
  obj: Record<string, any>,
  idKey = 'id',
) {
  const newArr: unknown[] = [];
  state[arrKey].forEach((arrItem: Record<string, any>) => {
    if (!(obj[idKey] === arrItem[idKey])) {
      newArr.push(arrItem);
    }
  });
  return { ...state, [arrKey]: newArr };
}

/**
 * 从指定数组中获取具有指定标识的对象。
 *
 * @param arr 数组。
 * @param id 标识。
 */
export function getFromArr(arr: Record<string, any>[], id: string) {
  let obj;
  arr.forEach(o => {
    if (o.id === id) {
      obj = o;
    }
  });
  return obj;
}

/**
 * 添加指定对象到指定索引 arrKey 处的对象中。
 *
 * @param state
 * @param arrKey
 * @param obj
 * @param prepend
 */
export function addToArr(
  state: Record<string, any>,
  arrKey: string,
  obj: Record<string, any>,
  prepend = false,
) {
  const newObj = { ...obj };
  if (!newObj.id) {
    newObj.id = shortid.generate();
  }
  const newState = {};
  if (prepend) {
    newState[arrKey] = [newObj, ...state[arrKey]];
  } else {
    newState[arrKey] = [...state[arrKey], newObj];
  }
  return { ...state, ...newState };
}

/**
 * 展开数组并添加到指定索引 arrKey 处。
 *
 * @param state
 * @param arrKey
 * @param arr 数组。
 * @param prepend
 */
export function extendArr(
  state: Record<string, any>,
  arrKey: string,
  arr: Record<string, any>[],
  prepend = false,
) {
  const newArr = [...arr];
  newArr.forEach(el => {
    if (!el.id) {
      /* eslint-disable no-param-reassign */
      el.id = shortid.generate();
    }
  });
  const newState = {};
  if (prepend) {
    newState[arrKey] = [...newArr, ...state[arrKey]];
  } else {
    newState[arrKey] = [...state[arrKey], ...newArr];
  }
  return { ...state, ...newState };
}

/**
 * 初始化增强器。
 *
 * @param persist 是否持久化。
 * @param persistConfig 持久化配置。
 */
export function initEnhancer(
  persist = true,
  persistConfig: { paths?: StorageAdapter<unknown>; config?: string } = {},
) {
  const { paths, config } = persistConfig;
  const composeEnhancers =
    process.env.WEBPACK_MODE === 'development'
      ? /* eslint-disable-next-line no-underscore-dangle, dot-notation */
        window['__REDUX_DEVTOOLS_EXTENSION_COMPOSE__'] || compose
      : compose;

  return persist
    ? composeEnhancers(persistState(paths, config))
    : composeEnhancers();
}

export function areArraysShallowEqual(arr1: unknown[], arr2: unknown[]) {
  // returns whether 2 arrays are shallow equal
  // used in shouldComponentUpdate when denormalizing arrays
  // where the array object is different every time, but the content might
  // be the same
  if (!arr1 || !arr2) {
    return false;
  }
  if (arr1.length !== arr2.length) {
    return false;
  }
  const { length } = arr1;
  for (let i = 0; i < length; i += 1) {
    if (arr1[i] !== arr2[i]) {
      return false;
    }
  }
  return true;
}

export function areObjectsEqual(
  obj1: any,
  obj2: any,
  opts = { ignoreUndefined: false },
) {
  let comp1 = obj1;
  let comp2 = obj2;
  if (opts.ignoreUndefined) {
    comp1 = omitBy(obj1, isUndefined);
    comp2 = omitBy(obj2, isUndefined);
  }
  return isEqual(comp1, comp2);
}
