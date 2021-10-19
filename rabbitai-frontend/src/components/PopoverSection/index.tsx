import React, { MouseEventHandler, ReactNode } from 'react';
import { useTheme } from '@superset-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import Icons from 'src/components/Icons';

export interface PopoverSectionProps {
  title: string;
  isSelected?: boolean;
  onSelect?: MouseEventHandler<HTMLDivElement>;
  info?: string;
  children?: ReactNode;
}

export default function PopoverSection({
  title,
  isSelected,
  children,
  onSelect,
  info,
}: PopoverSectionProps) {
  const theme = useTheme();
  return (
    <div
      css={{
        paddingBottom: theme.gridUnit * 2,
        opacity: isSelected ? 1 : theme.opacity.mediumHeavy,
      }}
    >
      <div
        role="button"
        tabIndex={0}
        onClick={onSelect}
        css={{
          display: 'flex',
          alignItems: 'center',
          cursor: onSelect ? 'pointer' : 'default',
        }}
      >
        <strong data-test="popover-title">{title}</strong>
        {info && (
          <Tooltip title={info} css={{ marginLeft: theme.gridUnit }}>
            <Icons.InfoSolidSmall
              role="img"
              width={14}
              height={14}
              iconColor={theme.colors.grayscale.light1}
            />
          </Tooltip>
        )}
        <Icons.Check
          role="img"
          iconColor={
            isSelected ? theme.colors.primary.base : theme.colors.grayscale.base
          }
        />
      </div>
      <div
        css={{
          marginLeft: theme.gridUnit,
          marginTop: theme.gridUnit,
        }}
      >
        {children}
      </div>
    </div>
  );
}
