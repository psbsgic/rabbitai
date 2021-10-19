import React from 'react';
import Card, { CardProps } from '.';

export default {
  title: 'Card',
  component: Card,
};

export const InteractiveCard = (args: CardProps) => <Card {...args} />;

InteractiveCard.args = {
  padded: true,
  title: 'Card title',
  children: 'Card content',
  bordered: true,
  loading: false,
  hoverable: false,
};

InteractiveCard.argTypes = {
  onClick: {
    table: {
      disable: true,
    },
    action: 'onClick',
  },
  theme: {
    table: {
      disable: true,
    },
  },
};

InteractiveCard.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
