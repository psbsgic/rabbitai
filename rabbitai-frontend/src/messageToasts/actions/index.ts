import shortid from 'shortid';
import { ToastType, ToastMeta } from '../types';

type ToastOptions = Partial<Omit<ToastMeta, 'id' | 'toastType' | 'text'>>;

export function getToastUuid(type: ToastType) {
  return `${type}-${shortid.generate()}`;
}

export const ADD_TOAST = 'ADD_TOAST';
export function addToast({
  toastType,
  text,
  duration = 8000,
  noDuplicate = false,
}: Omit<ToastMeta, 'id'>) {
  return {
    type: ADD_TOAST,
    payload: {
      id: getToastUuid(toastType),
      toastType,
      text,
      duration,
      noDuplicate,
    },
  };
}

export const REMOVE_TOAST = 'REMOVE_TOAST';
export function removeToast(id: string) {
  return {
    type: REMOVE_TOAST,
    payload: {
      id,
    },
  };
}

// Different types of toasts
export const ADD_INFO_TOAST = 'ADD_INFO_TOAST';
export function addInfoToast(text: string, options?: ToastOptions) {
  return addToast({
    text,
    toastType: ToastType.INFO,
    duration: 4000,
    ...options,
  });
}

export const ADD_SUCCESS_TOAST = 'ADD_SUCCESS_TOAST';
export function addSuccessToast(text: string, options?: ToastOptions) {
  return addToast({
    text,
    toastType: ToastType.SUCCESS,
    duration: 4000,
    ...options,
  });
}

export const ADD_WARNING_TOAST = 'ADD_WARNING_TOAST';
export function addWarningToast(text: string, options?: ToastOptions) {
  return addToast({
    text,
    toastType: ToastType.WARNING,
    duration: 6000,
    ...options,
  });
}

export const ADD_DANGER_TOAST = 'ADD_DANGER_TOAST';
export function addDangerToast(text: string, options?: ToastOptions) {
  return addToast({
    text,
    toastType: ToastType.DANGER,
    duration: 8000,
    ...options,
  });
}

export const toastActions = {
  addInfoToast,
  addSuccessToast,
  addWarningToast,
  addDangerToast,
};
