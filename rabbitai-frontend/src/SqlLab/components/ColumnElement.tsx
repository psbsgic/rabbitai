
import React from 'react';
import PropTypes from 'prop-types';
import { ClassNames } from '@emotion/react';
import { styled, useTheme } from '@rabbitai-ui/core';

import { Tooltip } from 'src/components/Tooltip';

const propTypes = {
  column: PropTypes.object.isRequired,
};

const StyledTooltip = (props: any) => {
  const theme = useTheme();
  return (
    <ClassNames>
      {({ css }) => (
        <Tooltip
          overlayClassName={css`
            .ant-tooltip-inner {
              max-width: ${theme.gridUnit * 125}px;
              word-wrap: break-word;
              text-align: center;

              pre {
                background: transparent;
                border: none;
                text-align: left;
                color: ${theme.colors.grayscale.light5};
                font-size: ${theme.typography.sizes.xs}px;
              }
            }
          `}
          {...props}
        />
      )}
    </ClassNames>
  );
};

const Hr = styled.hr`
  margin-top: ${({ theme }) => theme.gridUnit * 1.5}px;
`;

const iconMap = {
  pk: 'fa-key',
  fk: 'fa-link',
  index: 'fa-bookmark',
};
const tooltipTitleMap = {
  pk: 'Primary key',
  fk: 'Foreign key',
  index: 'Index',
};

export type ColumnKeyTypeType = keyof typeof tooltipTitleMap;

interface ColumnElementProps {
  column: {
    name: string;
    keys?: { type: ColumnKeyTypeType }[];
    type: string;
  };
}

export default function ColumnElement({ column }: ColumnElementProps) {
  let columnName: React.ReactNode = column.name;
  let icons;
  if (column.keys && column.keys.length > 0) {
    columnName = <strong>{column.name}</strong>;
    icons = column.keys.map((key, i) => (
      <span key={i} className="ColumnElement">
        <StyledTooltip
          placement="right"
          title={
            <>
              <strong>{tooltipTitleMap[key.type]}</strong>
              <Hr />
              <pre className="text-small">
                {JSON.stringify(key, null, '  ')}
              </pre>
            </>
          }
        >
          <i className={`fa text-muted m-l-2 ${iconMap[key.type]}`} />
        </StyledTooltip>
      </span>
    ));
  }
  return (
    <div className="clearfix table-column">
      <div className="pull-left m-l-10 col-name">
        {columnName}
        {icons}
      </div>
      <div className="pull-right text-muted">
        <small> {column.type}</small>
      </div>
    </div>
  );
}
ColumnElement.propTypes = propTypes;
