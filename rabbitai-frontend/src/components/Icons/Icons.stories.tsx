
import React from 'react';
import { styled, rabbitaiTheme } from '@rabbitai-ui/core';
import Icons from '.';
import IconType from './IconType';
import Icon from './Icon';

export default {
  title: 'Icons',
  component: Icon,
};

const palette = { Default: null };
Object.entries(rabbitaiTheme.colors).forEach(([familyName, family]) => {
  Object.entries(family).forEach(([colorName, colorValue]) => {
    palette[`${familyName} / ${colorName}`] = colorValue;
  });
});

const IconSet = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, 200px);
  grid-auto-rows: 100px;
`;

const IconBlock = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: ${({ theme }) => theme.gridUnit * 2}px;
`;

export const InteractiveIcons = ({
  showNames,
  ...rest
}: IconType & { showNames: boolean }) => (
  <IconSet>
    {Object.keys(Icons).map(k => {
      const IconComponent = Icons[k];
      return (
        <IconBlock key={k}>
          <IconComponent {...rest} />
          {showNames && k}
        </IconBlock>
      );
    })}
  </IconSet>
);

InteractiveIcons.argTypes = {
  showNames: {
    name: 'Show names',
    defaultValue: true,
    control: { type: 'boolean' },
  },
  iconSize: {
    defaultValue: 'xl',
    control: { type: 'inline-radio' },
  },
  iconColor: {
    defaultValue: null,
    control: { type: 'select', options: palette },
  },
  // @TODO twoToneColor is being ignored
  twoToneColor: {
    defaultValue: null,
    control: { type: 'select', options: palette },
  },
  theme: {
    table: {
      disable: true,
    },
  },
};

InteractiveIcons.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
