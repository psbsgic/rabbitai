import React from 'react';
import { action } from '@storybook/addon-actions';
import Label, { Type } from './index';

export default {
  title: 'Label',
  component: Label,
  excludeStories: 'options',
};

export const options = [
  'default',
  'info',
  'success',
  'warning',
  'danger',
  'primary',
  'secondary',
];

export const LabelGallery = () => (
  <>
    <h4>Non-interactive</h4>
    {Object.values(options).map((opt: Type) => (
      <Label key={opt} type={opt}>
        {`style: "${opt}"`}
      </Label>
    ))}
    <br />
    <h4>Interactive</h4>
    {Object.values(options).map((opt: Type) => (
      <Label key={opt} type={opt} onClick={action('clicked')}>
        {`style: "${opt}"`}
      </Label>
    ))}
  </>
);

export const InteractiveLabel = (args: any) => {
  const { hasOnClick, label, ...rest } = args;
  return (
    <Label onClick={hasOnClick ? action('clicked') : undefined} {...rest}>
      {label}
    </Label>
  );
};

InteractiveLabel.args = {
  hasOnClick: true,
  label: 'Example',
};
