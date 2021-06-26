
import { useToasts } from 'src/messageToasts/enhancers/withToasts';
import { useComponentDidMount } from 'src/common/hooks/useComponentDidMount';

type FlashMessageType = 'info' | 'alert' | 'danger' | 'warning' | 'success';
export type FlashMessage = [FlashMessageType, string];

interface Props {
  children: JSX.Element;
  messages: FlashMessage[];
}

const flashObj = {
  info: 'addInfoToast',
  alert: 'addDangerToast',
  danger: 'addDangerToast',
  warning: 'addWarningToast',
  success: 'addSuccessToast',
};

export default function FlashProvider({ children, messages }: Props) {
  const toasts = useToasts();
  useComponentDidMount(() => {
    messages.forEach(message => {
      const [type, text] = message;
      const flash = flashObj[type];
      const toast = toasts[flash];
      if (toast) {
        toast(text);
      }
    });
  });
  return children;
}
