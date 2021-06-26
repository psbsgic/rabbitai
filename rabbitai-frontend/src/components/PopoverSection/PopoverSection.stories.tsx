
import React from 'react';
import PopoverSection from '.';

export default {
  title: 'PopoverSection',
};

export const InteractivePopoverSection = (args: any) => (
  <PopoverSection {...args}>
    <div
      css={{
        display: 'flex',
        justifyContent: 'center',
        border: '1px solid',
        alignItems: 'center',
        width: 100,
        height: 100,
      }}
    >
      Content
    </div>
  </PopoverSection>
);

InteractivePopoverSection.args = {
  title: 'Title',
  isSelected: true,
  info: 'Some description about the content',
};

InteractivePopoverSection.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
