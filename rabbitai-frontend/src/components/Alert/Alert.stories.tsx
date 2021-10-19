import React from 'react';
import Alert, { AlertProps } from './index';

type AlertType = Pick<AlertProps, 'type'>;
type AlertTypeValue = AlertType[keyof AlertType];

const types: AlertTypeValue[] = ['info', 'error', 'warning', 'success'];

const smallText = 'Lorem ipsum dolor sit amet';

const bigText =
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' +
  'Nam id porta neque, a vehicula orci. Maecenas rhoncus elit sit amet ' +
  'purus convallis placerat in at nunc. Nulla nec viverra augue.';

export default {
  title: 'Alert',
  component: Alert,
};

export const AlertGallery = () => (
  <>
    {types.map(type => (
      <div key={type} style={{ marginBottom: 40, width: 600 }}>
        <h4>{type}</h4>
        <Alert
          type={type}
          showIcon
          closable
          message={bigText}
          style={{ marginBottom: 20 }}
        />
        <Alert
          type={type}
          showIcon
          message={smallText}
          description={bigText}
          closable
        />
      </div>
    ))}
  </>
);

AlertGallery.story = {
  parameters: {
    actions: {
      disable: true,
    },
    controls: {
      disable: true,
    },
    knobs: {
      disable: true,
    },
  },
};

export const InteractiveAlert = (args: AlertProps) => (
  <>
    <Alert {...args} />
    Some content to test the `roomBelow` prop
  </>
);

InteractiveAlert.args = {
  closable: true,
  roomBelow: false,
  type: 'info',
  message: smallText,
  description: bigText,
  showIcon: true,
};

InteractiveAlert.argTypes = {
  onClose: { action: 'onClose' },
  type: {
    control: { type: 'select', options: types },
  },
};

InteractiveAlert.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
