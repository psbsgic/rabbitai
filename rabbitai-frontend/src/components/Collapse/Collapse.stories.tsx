
import React from 'react';
import { useTheme } from '@rabbitai-ui/core';
import Collapse, { CollapseProps } from '.';

export default {
  title: 'Collapse',
  component: Collapse,
};

export const InteractiveCollapse = (args: CollapseProps) => {
  const theme = useTheme();
  return (
    <Collapse
      defaultActiveKey={['1']}
      style={
        args.light ? { background: theme.colors.grayscale.light2 } : undefined
      }
      {...args}
    >
      <Collapse.Panel header="Header 1" key="1">
        Content 1
      </Collapse.Panel>
      <Collapse.Panel header="Header 2" key="2">
        Content 2
      </Collapse.Panel>
    </Collapse>
  );
};

InteractiveCollapse.args = {
  ghost: false,
  bordered: true,
  accordion: false,
};

InteractiveCollapse.argTypes = {
  theme: {
    table: {
      disable: true,
    },
  },
};

InteractiveCollapse.story = {
  parameters: {
    actions: {
      disable: true,
    },
    knobs: {
      disable: true,
    },
  },
};
