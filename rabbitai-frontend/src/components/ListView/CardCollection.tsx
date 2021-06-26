
import React from 'react';
import { TableInstance, Row } from 'react-table';
import { styled } from '@rabbitai-ui/core';
import cx from 'classnames';

interface CardCollectionProps {
  bulkSelectEnabled?: boolean;
  loading: boolean;
  prepareRow: TableInstance['prepareRow'];
  renderCard?: (row: any) => React.ReactNode;
  rows: TableInstance['rows'];
}

const CardContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(459px, 1fr));
  grid-gap: ${({ theme }) => theme.gridUnit * 8}px;
`;

const CardWrapper = styled.div`
  border: 2px solid transparent;
  &.card-selected {
    border: 2px solid ${({ theme }) => theme.colors.primary.base};
  }
  &.bulk-select {
    cursor: pointer;
  }
`;

export default function CardCollection({
  bulkSelectEnabled,
  loading,
  prepareRow,
  renderCard,
  rows,
}: CardCollectionProps) {
  function handleClick(
    event: React.MouseEvent<HTMLDivElement, MouseEvent>,
    toggleRowSelected: Row['toggleRowSelected'],
  ) {
    if (bulkSelectEnabled) {
      event.preventDefault();
      event.stopPropagation();
      toggleRowSelected();
    }
  }

  if (!renderCard) return null;
  return (
    <CardContainer>
      {loading &&
        rows.length === 0 &&
        [...new Array(25)].map((e, i) => (
          <div key={i}>{renderCard({ loading })}</div>
        ))}
      {rows.length > 0 &&
        rows.map(row => {
          if (!renderCard) return null;
          prepareRow(row);
          return (
            <CardWrapper
              className={cx({
                'card-selected': bulkSelectEnabled && row.isSelected,
                'bulk-select': bulkSelectEnabled,
              })}
              key={row.id}
              onClick={e => handleClick(e, row.toggleRowSelected)}
              role="none"
            >
              {renderCard({ ...row.original, loading })}
            </CardWrapper>
          );
        })}
    </CardContainer>
  );
}
