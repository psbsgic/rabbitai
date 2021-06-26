
import { styled, t } from '@rabbitai-ui/core';
import React from 'react';
import { Tooltip } from 'src/components/Tooltip';
import Icon, { IconName } from 'src/components/Icon';
import { RecipientIconName } from '../types';

const StyledIcon = styled(Icon)`
  color: ${({ theme }) => theme.colors.grayscale.light1};
  margin-right: ${({ theme }) => theme.gridUnit * 2}px;
`;

export default function RecipientIcon({ type }: { type: string }) {
  const recipientIconConfig = {
    name: '',
    label: '',
  };
  switch (type) {
    case RecipientIconName.email:
      recipientIconConfig.name = 'email';
      recipientIconConfig.label = t(`${RecipientIconName.email}`);
      break;
    case RecipientIconName.slack:
      recipientIconConfig.name = 'slack';
      recipientIconConfig.label = t(`${RecipientIconName.slack}`);
      break;
    default:
      recipientIconConfig.name = '';
      recipientIconConfig.label = '';
  }
  return recipientIconConfig.name.length ? (
    <Tooltip title={recipientIconConfig.label} placement="bottom">
      <StyledIcon name={recipientIconConfig.name as IconName} />
    </Tooltip>
  ) : null;
}
