import React from 'react';
import ModalTrigger from '.';

interface IModalTriggerProps {
  triggerNode: React.ReactNode;
  dialogClassName?: string;
  modalTitle?: React.ReactNode;
  modalBody?: React.ReactNode;
  modalFooter?: React.ReactNode;
  beforeOpen?: () => void;
  onExit?: () => void;
  isButton?: boolean;
  className?: string;
  tooltip?: string;
  width?: string;
  maxWidth?: string;
  responsive?: boolean;
}

export default {
  title: 'ModalTrigger',
  component: ModalTrigger,
};

export const InteractiveModalTrigger = (args: IModalTriggerProps) => (
  <ModalTrigger triggerNode={<span>Click me</span>} {...args} />
);

InteractiveModalTrigger.args = {
  isButton: true,
  modalTitle: 'I am a modal title',
  modalBody: 'I am a modal body',
  modalFooter: 'I am a modal footer',
  tooltip: 'I am a tooltip',
  width: '600px',
  maxWidth: '1000px',
  responsive: true,
};
