
import React from 'react';
import AnchorLink from '.';

export default {
  title: 'AnchorLink',
  component: AnchorLink,
};

export const InteractiveAnchorLink = (args: any) => (
  <AnchorLink anchorLinkId="link" {...args} />
);

const PLACEMENTS = ['right', 'left', 'top', 'bottom'];

InteractiveAnchorLink.args = {
  showShortLinkButton: true,
  placement: PLACEMENTS[0],
};

InteractiveAnchorLink.argTypes = {
  type: {
    placement: { type: 'select', options: PLACEMENTS },
  },
};

InteractiveAnchorLink.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
