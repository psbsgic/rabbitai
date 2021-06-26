
import React from 'react';
import Button from 'src/components/Button';
import Icon from 'src/components/Icon';
import ToastPresenter from 'src/messageToasts/containers/ToastPresenter';
import CopyToClipboard from '.';

export default {
  title: 'CopyToClipboard',
  component: CopyToClipboard,
};

export const InteractiveCopyToClipboard = ({ copyNode, ...rest }: any) => {
  let node = <Button>Copy</Button>;
  if (copyNode === 'Icon') {
    node = <Icon name="copy" />;
  } else if (copyNode === 'Text') {
    node = <span role="button">Copy</span>;
  }
  return (
    <>
      <CopyToClipboard copyNode={node} {...rest} />
      <ToastPresenter />
    </>
  );
};

InteractiveCopyToClipboard.args = {
  shouldShowText: true,
  text: 'http://rabbitai.apache.org/',
  wrapped: true,
  tooltipText: 'Copy to clipboard',
};

InteractiveCopyToClipboard.argTypes = {
  onCopyEnd: { action: 'onCopyEnd' },
  copyNode: {
    defaultValue: 'Button',
    control: { type: 'radio', options: ['Button', 'Icon', 'Text'] },
  },
};

InteractiveCopyToClipboard.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
