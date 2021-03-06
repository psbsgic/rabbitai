import React from 'react';
import { withKnobs, select } from '@storybook/addon-knobs';
import { styled, supersetTheme } from '@superset-ui/core';
import Icon, { iconsRegistry } from '.';

export default {
  title: 'Icon',
  component: Icon,
  decorators: [withKnobs],
};

const palette = {};
Object.entries(supersetTheme.colors).forEach(([familyName, family]) => {
  Object.entries(family).forEach(([colorName, colorValue]) => {
    palette[`${familyName} / ${colorName}`] = colorValue;
  });
});

const colorKnob = {
  label: 'Color',
  options: {
    Default: null,
    ...palette,
  },
  defaultValue: null,
};

const IconSet = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
`;

const IconBlock = styled.div`
  flex-grow: 0;
  flex-shrink: 0;
  flex-basis: 10%;
  text-align: center;
  padding: ${({ theme }) => theme.gridUnit * 2}px;
  div {
    white-space: nowrap;
    font-size: ${({ theme }) => theme.typography.sizes.s}px;
  }
`;

export const RabbitaiIcon = () => (
  <IconSet>
    {Object.keys(iconsRegistry)
      .sort()
      .map(iconName => (
        <IconBlock key={iconName}>
          <Icon
            name={iconName}
            key={iconName}
            color={select(
              colorKnob.label,
              colorKnob.options,
              colorKnob.defaultValue,
              colorKnob.groupId,
            )}
          />
          <div>{iconName}</div>
        </IconBlock>
      ))}
  </IconSet>
);
