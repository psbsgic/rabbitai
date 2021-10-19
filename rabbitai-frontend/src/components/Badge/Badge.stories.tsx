import React from 'react';
import Badge, { BadgeProps } from '.';

export default {
  title: 'Badge',
  component: Badge,
};

type BadgeColor = Pick<BadgeProps, 'color'>;
type BadgeColorValue = BadgeColor[keyof BadgeColor];
type BadgeSize = Pick<BadgeProps, 'size'>;
type BadgeSizeValue = BadgeSize[keyof BadgeSize];

const badgeColors: BadgeColorValue[] = [
  'pink',
  'red',
  'yellow',
  'orange',
  'cyan',
  'green',
  'blue',
  'purple',
  'geekblue',
  'magenta',
  'volcano',
  'gold',
  'lime',
];
const badgeSizes: BadgeSizeValue[] = ['default', 'small'];
const STATUSES = ['default', 'error', 'warning', 'success', 'processing'];

const COLORS = {
  label: 'colors',
  options: badgeColors,
  defaultValue: undefined,
};

const SIZES = {
  label: 'sizes',
  options: badgeSizes,
  defaultValue: undefined,
};

export const InteractiveBadge = (args: BadgeProps) => <Badge {...args} />;

InteractiveBadge.args = {
  count: null,
  color: null,
  text: 'Text',
  textColor: null,
  status: 'success',
  size: 'default',
};

InteractiveBadge.argTypes = {
  status: {
    control: {
      type: 'select',
      options: [undefined, ...STATUSES],
    },
  },
  size: {
    control: {
      type: 'select',
      options: SIZES.options,
    },
  },
  color: {
    control: {
      type: 'select',
      options: [undefined, ...COLORS.options],
    },
  },
  textColor: {
    control: {
      type: 'select',
      options: [undefined, ...COLORS.options],
    },
  },
  count: {
    control: {
      type: 'select',
      options: [undefined, ...Array(100).keys()],
    },
  },
};

InteractiveBadge.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};

export const BadgeGallery = () => (
  <>
    {SIZES.options.map(size => (
      <div key={size} style={{ marginBottom: 40 }}>
        <h4>{size}</h4>
        {COLORS.options.map(color => (
          <Badge
            count={9}
            textColor={color}
            size={size}
            key={`${color}_${size}`}
            style={{ marginRight: '15px' }}
          />
        ))}
      </div>
    ))}
  </>
);

export const BadgeTextGallery = () => (
  <>
    {COLORS.options.map(color => (
      <Badge
        text="Hello"
        color={color}
        key={color}
        style={{ marginRight: '15px' }}
      />
    ))}
  </>
);

BadgeGallery.story = {
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

BadgeTextGallery.story = {
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
