import React from 'react';
import Loading, { Props, PositionOption } from './index';

export default {
  title: 'Loading',
  component: Loading,
  includeStories: ['LoadingGallery', 'InteractiveLoading'],
};

export const POSITIONS: PositionOption[] = ['normal', 'floating', 'inline'];

export const LoadingGallery = () => (
  <>
    {POSITIONS.map(position => (
      <div
        key={position}
        style={{
          marginBottom: 60,
          borderBottom: '1px solid #000',
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <h4>{position}</h4>
        <Loading position={position} image="/images/loading.gif" />
      </div>
    ))}
  </>
);

LoadingGallery.story = {
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

export const InteractiveLoading = (args: Props) => <Loading {...args} />;

InteractiveLoading.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};

InteractiveLoading.args = {
  image: '/images/loading.gif',
  className: '',
};

InteractiveLoading.argTypes = {
  position: {
    name: 'position',
    control: { type: 'select', options: POSITIONS },
  },
};
