
import React, { useState } from 'react';
import DeleteModal from 'src/components/DeleteModal';

export type Callback = (...args: any[]) => void;

export interface ConfirmStatusChangeProps {
  title: React.ReactNode;
  description: React.ReactNode;
  onConfirm: Callback;
  children: (showConfirm: Callback) => React.ReactNode;
}

export default function ConfirmStatusChange({
  title,
  description,
  onConfirm,
  children,
}: ConfirmStatusChangeProps) {
  const [open, setOpen] = useState(false);
  const [currentCallbackArgs, setCurrentCallbackArgs] = useState<any[]>([]);

  const showConfirm = (...callbackArgs: any[]) => {
    // check if any args are DOM events, if so, call persist
    callbackArgs.forEach(arg => {
      if (!arg) {
        return;
      }
      if (typeof arg.persist === 'function') {
        arg.persist();
      }
      if (typeof arg.preventDefault === 'function') {
        arg.preventDefault();
      }
      if (typeof arg.stopPropagation === 'function') {
        arg.stopPropagation();
      }
    });
    setOpen(true);
    setCurrentCallbackArgs(callbackArgs);
  };

  const hide = () => {
    setOpen(false);
    setCurrentCallbackArgs([]);
  };

  const confirm = () => {
    onConfirm(...currentCallbackArgs);
    hide();
  };

  return (
    <>
      {children && children(showConfirm)}
      <DeleteModal
        description={description}
        onConfirm={confirm}
        onHide={hide}
        open={open}
        title={title}
      />
    </>
  );
}
