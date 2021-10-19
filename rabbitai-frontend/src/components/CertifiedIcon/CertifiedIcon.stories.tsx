import React from 'react';
import CertifiedIcon, { CertifiedIconProps } from '.';

export default {
  title: 'CertifiedIconWithTooltip',
};

export const InteractiveIcon = (args: CertifiedIconProps) => (
  <CertifiedIcon {...args} />
);

InteractiveIcon.args = {
  certifiedBy: 'Trusted Authority',
  details: 'All requirements have been met.',
  size: 30,
};

InteractiveIcon.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
