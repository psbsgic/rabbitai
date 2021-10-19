import React from 'react';
import AlteredSliceTag from '.';
import { defaultProps } from './AlteredSliceTagMocks';

export default {
  title: 'AlteredSliceTag',
};

export const InteractiveSliceTag = (args: any) => <AlteredSliceTag {...args} />;

InteractiveSliceTag.args = {
  origFormData: defaultProps.origFormData,
  currentFormData: defaultProps.currentFormData,
};

InteractiveSliceTag.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
