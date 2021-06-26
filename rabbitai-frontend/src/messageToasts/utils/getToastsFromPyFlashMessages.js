
import { addToast } from '../actions';
import { ToastType } from '../constants';

export default function toastsFromPyFlashMessages(flashMessages = []) {
  const toasts = [];

  flashMessages.forEach(([messageType, message]) => {
    const toastType =
      messageType === 'danger'
        ? ToastType.DANGER
        : (messageType === 'success' && ToastType.SUCCESS) || ToastType.INFO;

    const toast = addToast({
      text: message,
      toastType,
    }).payload;

    toasts.push(toast);
  });

  return toasts;
}
