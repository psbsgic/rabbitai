import { t, SupersetTheme, css } from '@superset-ui/core';
import React, { ReactElement } from 'react';
import { Tooltip } from 'src/components/Tooltip';
import Icons from 'src/components/Icons';
import { RecipientIconName } from '../types';

const StyledIcon = (theme: SupersetTheme) => css`
  color: ${theme.colors.grayscale.light1};
  margin-right: ${theme.gridUnit * 2}px;
`;

export default function RecipientIcon({ type }: { type: string }) {
  const recipientIconConfig: { icon: null | ReactElement; label: string } = {
    icon: null,
    label: '',
  };
  switch (type) {
    case RecipientIconName.email:
      recipientIconConfig.icon = <Icons.Email css={StyledIcon} />;
      recipientIconConfig.label = t(`${RecipientIconName.email}`);
      break;
    case RecipientIconName.slack:
      recipientIconConfig.icon = <Icons.Slack css={StyledIcon} />;
      recipientIconConfig.label = t(`${RecipientIconName.slack}`);
      break;
    default:
      recipientIconConfig.icon = null;
      recipientIconConfig.label = '';
  }
  return recipientIconConfig.icon ? (
    <Tooltip title={recipientIconConfig.label} placement="bottom">
      {recipientIconConfig.icon}
    </Tooltip>
  ) : null;
}
