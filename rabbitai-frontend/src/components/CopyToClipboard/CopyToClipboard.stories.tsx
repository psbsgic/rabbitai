import React from 'react';
import { useTheme } from '@superset-ui/core';
import Button from 'src/components/Button';
import Icons from 'src/components/Icons';
import ToastPresenter from 'src/messageToasts/containers/ToastPresenter';
import CopyToClipboard from '.';

export default {
  title: 'CopyToClipboard',
  component: CopyToClipboard,
};

export const InteractiveCopyToClipboard = ({ copyNode, ...rest }: any) => {
  const theme = useTheme();
  let node = <Button>Copy</Button>;
  if (copyNode === 'Icon') {
    node = <Icons.Copy iconColor={theme.colors.grayscale.base} />;
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
