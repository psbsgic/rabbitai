
import React from 'react';
import {
  getCategoricalSchemeRegistry,
  styled,
  RabbitaiTheme,
} from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import { Avatar } from 'src/common/components';
import { getRandomColor } from './utils';

interface FacePileProps {
  users: { first_name: string; last_name: string; id: number }[];
  maxCount?: number;
}

const colorList = getCategoricalSchemeRegistry().get()?.colors ?? [];

const customAvatarStyler = (theme: RabbitaiTheme) => `
  width: ${theme.gridUnit * 6}px;
  height: ${theme.gridUnit * 6}px;
  line-height: ${theme.gridUnit * 6}px;
  font-size: ${theme.typography.sizes.m}px;
`;

const StyledAvatar = styled(Avatar)`
  ${({ theme }) => customAvatarStyler(theme)}
`;

// to apply styling to the maxCount avatar
const StyledGroup = styled(Avatar.Group)`
  .ant-avatar {
    ${({ theme }) => customAvatarStyler(theme)}
  }
`;

export default function FacePile({ users, maxCount = 4 }: FacePileProps) {
  return (
    <StyledGroup maxCount={maxCount}>
      {users.map(({ first_name, last_name, id }) => {
        const name = `${first_name} ${last_name}`;
        const uniqueKey = `${id}-${first_name}-${last_name}`;
        const color = getRandomColor(uniqueKey, colorList);
        return (
          <Tooltip key={name} title={name} placement="top">
            <StyledAvatar
              key={name}
              style={{
                backgroundColor: color,
                borderColor: color,
              }}
            >
              {first_name && first_name[0]?.toLocaleUpperCase()}
              {last_name && last_name[0]?.toLocaleUpperCase()}
            </StyledAvatar>
          </Tooltip>
        );
      })}
    </StyledGroup>
  );
}
