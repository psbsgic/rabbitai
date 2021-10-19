import React from 'react';
import AsyncEsmComponent, { PlaceholderProps } from '.';

export default {
  title: 'AsyncEsmComponent',
};

const Placeholder = () => <span>Loading...</span>;

const AsyncComponent = ({ bold }: { bold: boolean }) => (
  <span style={{ fontWeight: bold ? 700 : 400 }}>AsyncComponent</span>
);

const Component = AsyncEsmComponent(
  new Promise(resolve => setTimeout(() => resolve(AsyncComponent), 3000)),
  Placeholder,
);

export const InteractiveEsmComponent = (args: PlaceholderProps) => (
  <Component {...args} showLoadingForImport />
);

InteractiveEsmComponent.args = {
  bold: true,
};

InteractiveEsmComponent.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
