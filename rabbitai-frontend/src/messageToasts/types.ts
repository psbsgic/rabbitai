
export enum ToastType {
  INFO = 'INFO_TOAST',
  SUCCESS = 'SUCCESS_TOAST',
  WARNING = 'WARNING_TOAST',
  DANGER = 'DANGER_TOAST',
}

export interface ToastMeta {
  id: string;
  toastType: ToastType;
  text: string;
  duration: number;
  /** Whether to skip displaying this message if there are another toast
   * with the same message. */
  noDuplicate?: boolean;
}
