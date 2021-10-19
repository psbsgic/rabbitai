import React from 'react';
import Button from 'src/components/Button';
import { Empty } from 'src/common/components';
import { t, styled } from '@superset-ui/core';

interface EmptyStateProps {
  tableName: string;
  tab?: string;
}
const EmptyContainer = styled.div`
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
`;
const ButtonContainer = styled.div`
  Button {
    svg {
      color: ${({ theme }) => theme.colors.grayscale.light5};
    }
  }
`;

export default function EmptyState({ tableName, tab }: EmptyStateProps) {
  const mineRedirects = {
    DASHBOARDS: '/dashboard/new',
    CHARTS: '/chart/add',
    SAVED_QUERIES: '/rabbitai/sqllab?new=true',
  };
  const favRedirects = {
    DASHBOARDS: '/dashboard/list/',
    CHARTS: '/chart/list',
    SAVED_QUERIES: '/savedqueryview/list/',
  };
  const tableIcon = {
    RECENTS: 'union.svg',
    DASHBOARDS: 'empty-dashboard.svg',
    CHARTS: 'empty-charts.svg',
    SAVED_QUERIES: 'empty-queries.svg',
  };
  const mine = (
    <span>{`No ${
      tableName === 'SAVED_QUERIES'
        ? t('saved queries')
        : t(`${tableName.toLowerCase()}`)
    } yet`}</span>
  );
  const recent = (
    <span className="no-recents">
      {(() => {
        if (tab === 'Viewed') {
          return t(
            `Recently viewed charts, dashboards, and saved queries will appear here`,
          );
        }
        if (tab === 'Created') {
          return t(
            'Recently created charts, dashboards, and saved queries will appear here',
          );
        }
        if (tab === 'Examples') {
          return t(`Example ${tableName.toLowerCase()} will appear here`);
        }
        if (tab === 'Edited') {
          return t(
            `Recently edited charts, dashboards, and saved queries will appear here`,
          );
        }
        return null;
      })()}
    </span>
  );
  // Mine and Recent Activity(all tabs) tab empty state
  if (tab === 'Mine' || tableName === 'RECENTS' || tab === 'Examples') {
    return (
      <EmptyContainer>
        <Empty
          image={`/static/assets/images/${tableIcon[tableName]}`}
          description={
            tableName === 'RECENTS' || tab === 'Examples' ? recent : mine
          }
        >
          {tableName !== 'RECENTS' && (
            <ButtonContainer>
              <Button
                buttonStyle="primary"
                onClick={() => {
                  window.location = mineRedirects[tableName];
                }}
              >
                <i className="fa fa-plus" />
                {tableName === 'SAVED_QUERIES'
                  ? t('SQL query')
                  : t(`${tableName
                      .split('')
                      .slice(0, tableName.length - 1)
                      .join('')}
                    `)}
              </Button>
            </ButtonContainer>
          )}
        </Empty>
      </EmptyContainer>
    );
  }
  // Favorite tab empty state
  return (
    <EmptyContainer>
      <Empty
        image="/static/assets/images/star-circle.svg"
        description={
          <span className="no-favorites">
            {t("You don't have any favorites yet!")}
          </span>
        }
      >
        <Button
          buttonStyle="primary"
          onClick={() => {
            window.location = favRedirects[tableName];
          }}
        >
          See all{' '}
          {tableName === 'SAVED_QUERIES'
            ? t('SQL Lab queries')
            : t(`${tableName}`)}
        </Button>
      </Empty>
    </EmptyContainer>
  );
}
