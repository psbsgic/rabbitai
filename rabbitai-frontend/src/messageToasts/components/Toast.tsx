
import { styled } from '@rabbitai-ui/core';
import cx from 'classnames';
import Interweave from 'interweave';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import Icon, { IconName } from 'src/components/Icon';
import { ToastType } from 'src/messageToasts/constants';
import { ToastMeta } from '../types';

const ToastContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;

  span {
    padding: 0 11px;
  }
`;

const StyledIcon = styled(Icon)`
  min-width: ${({ theme }) => theme.gridUnit * 5}px;
`;

interface ToastPresenterProps {
  toast: ToastMeta;
  onCloseToast: (id: string) => void;
}

export default function Toast({ toast, onCloseToast }: ToastPresenterProps) {
  const hideTimer = useRef<ReturnType<typeof setTimeout>>();
  const [visible, setVisible] = useState(false);
  const showToast = () => {
    setVisible(true);
  };

  const handleClosePress = useCallback(() => {
    if (hideTimer.current) {
      clearTimeout(hideTimer.current);
    }
    // Wait for the transition
    setVisible(() => {
      setTimeout(() => {
        onCloseToast(toast.id);
      }, 150);
      return false;
    });
  }, [onCloseToast, toast.id]);

  useEffect(() => {
    setTimeout(showToast);

    if (toast.duration > 0) {
      hideTimer.current = setTimeout(handleClosePress, toast.duration);
    }
    return () => {
      if (hideTimer.current) {
        clearTimeout(hideTimer.current);
      }
    };
  }, [handleClosePress, toast.duration]);

  let iconName: IconName = 'circle-check-solid';
  let className = 'toast--success';
  if (toast.toastType === ToastType.WARNING) {
    iconName = 'warning-solid';
    className = 'toast--warning';
  } else if (toast.toastType === ToastType.DANGER) {
    iconName = 'error-solid';
    className = 'toast--danger';
  } else if (toast.toastType === ToastType.INFO) {
    iconName = 'info-solid';
    className = 'toast--info';
  }

  return (
    <ToastContainer
      className={cx('alert', 'toast', visible && 'toast--visible', className)}
      data-test="toast-container"
      role="alert"
    >
      <StyledIcon name={iconName} />
      <Interweave content={toast.text} />
      <i
        className="fa fa-close pull-right pointer"
        role="button"
        tabIndex={0}
        onClick={handleClosePress}
        aria-label="Close"
        data-test="close-button"
      />
    </ToastContainer>
  );
}
