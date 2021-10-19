import React from 'react';
import Tabs, { TabsProps } from '.';

const { TabPane } = Tabs;

export default {
  title: 'Tabs',
  component: Tabs,
};

export const InteractiveTabs = (args: TabsProps) => (
  <Tabs {...args}>
    <TabPane tab="Tab 1" key="1">
      Content of Tab Pane 1
    </TabPane>
    <TabPane tab="Tab 2" key="2">
      Content of Tab Pane 2
    </TabPane>
    <TabPane tab="Tab 3" key="3">
      Content of Tab Pane 3
    </TabPane>
  </Tabs>
);

InteractiveTabs.args = {
  defaultActiveKey: '1',
  animated: true,
  centered: false,
  fullWidth: false,
  allowOverflow: false,
};

InteractiveTabs.argTypes = {
  onChange: { action: 'onChange' },
  type: {
    defaultValue: 'line',
    control: {
      type: 'inline-radio',
      options: ['line', 'card', 'editable-card'],
    },
  },
};

InteractiveTabs.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
