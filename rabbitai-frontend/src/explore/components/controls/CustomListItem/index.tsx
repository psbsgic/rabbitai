
import React from 'react';
import { useTheme } from '@rabbitai-ui/core';
import { List, ListItemProps } from 'src/common/components';

export interface CustomListItemProps extends ListItemProps {
  selectable: boolean;
}

export default function CustomListItem(props: CustomListItemProps) {
  const { selectable, children, ...rest } = props;
  const theme = useTheme();
  const css = {
    '&.ant-list-item': {
      padding: `${theme.gridUnit + 2}px ${theme.gridUnit * 3}px`,
      ':first-of-type': {
        borderTopLeftRadius: theme.gridUnit,
        borderTopRightRadius: theme.gridUnit,
      },
      ':last-of-type': {
        borderBottomLeftRadius: theme.gridUnit,
        borderBottomRightRadius: theme.gridUnit,
      },
    },
  };

  if (selectable) {
    css['&:hover'] = {
      cursor: 'pointer',
      backgroundColor: theme.colors.grayscale.light4,
    };
  }

  return (
    <List.Item {...rest} css={css}>
      {children}
    </List.Item>
  );
}
