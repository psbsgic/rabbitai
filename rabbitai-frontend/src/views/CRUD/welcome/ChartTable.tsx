
import React, { useState, useMemo, useEffect } from 'react';
import { t } from '@rabbitai-ui/core';
import {
  useListViewResource,
  useChartEditModal,
  useFavoriteStatus,
} from 'src/views/CRUD/hooks';
import {
  setInLocalStorage,
  getFromLocalStorage,
} from 'src/utils/localStorageHelpers';
import withToasts from 'src/messageToasts/enhancers/withToasts';
import { useHistory } from 'react-router-dom';
import PropertiesModal from 'src/explore/components/PropertiesModal';
import { User } from 'src/types/bootstrapTypes';
import ChartCard from 'src/views/CRUD/chart/ChartCard';
import Chart from 'src/types/Chart';
import Loading from 'src/components/Loading';
import ErrorBoundary from 'src/components/ErrorBoundary';
import SubMenu from 'src/components/Menu/SubMenu';
import EmptyState from './EmptyState';
import { CardContainer } from '../utils';

const PAGE_SIZE = 3;

interface ChartTableProps {
  addDangerToast: (message: string) => void;
  addSuccessToast: (message: string) => void;
  search: string;
  chartFilter?: string;
  user?: User;
  mine: Array<any>;
  showThumbnails: boolean;
}

function ChartTable({
  user,
  addDangerToast,
  addSuccessToast,
  mine,
  showThumbnails,
}: ChartTableProps) {
  const history = useHistory();
  const {
    state: { loading, resourceCollection: charts, bulkSelectEnabled },
    setResourceCollection: setCharts,
    hasPerm,
    refreshData,
    fetchData,
  } = useListViewResource<Chart>(
    'chart',
    t('chart'),
    addDangerToast,
    true,
    mine,
    [],
    false,
  );

  useEffect(() => {});
  const chartIds = useMemo(() => charts.map(c => c.id), [charts]);
  const [saveFavoriteStatus, favoriteStatus] = useFavoriteStatus(
    'chart',
    chartIds,
    addDangerToast,
  );
  const {
    sliceCurrentlyEditing,
    openChartEditModal,
    handleChartUpdated,
    closeChartEditModal,
  } = useChartEditModal(setCharts, charts);

  const [chartFilter, setChartFilter] = useState('Mine');

  useEffect(() => {
    const filter = getFromLocalStorage('chart', null);
    if (!filter) {
      setChartFilter('Mine');
    } else setChartFilter(filter.tab);
  }, []);

  const getFilters = (filterName: string) => {
    const filters = [];

    if (filterName === 'Mine') {
      filters.push({
        id: 'created_by',
        operator: 'rel_o_m',
        value: `${user?.userId}`,
      });
    } else {
      filters.push({
        id: 'id',
        operator: 'chart_is_favorite',
        value: true,
      });
    }
    return filters;
  };

  const getData = (filter: string) =>
    fetchData({
      pageIndex: 0,
      pageSize: PAGE_SIZE,
      sortBy: [
        {
          id: 'changed_on_delta_humanized',
          desc: true,
        },
      ],
      filters: getFilters(filter),
    });

  if (loading) return <Loading position="inline" />;
  return (
    <ErrorBoundary>
      {sliceCurrentlyEditing && (
        <PropertiesModal
          onHide={closeChartEditModal}
          onSave={handleChartUpdated}
          show
          slice={sliceCurrentlyEditing}
        />
      )}

      <SubMenu
        activeChild={chartFilter}
        // eslint-disable-next-line react/no-children-prop
        tabs={[
          {
            name: 'Favorite',
            label: t('Favorite'),
            onClick: () =>
              getData('Favorite').then(() => {
                setChartFilter('Favorite');
                setInLocalStorage('chart', { tab: 'Favorite' });
              }),
          },
          {
            name: 'Mine',
            label: t('Mine'),
            onClick: () =>
              getData('Mine').then(() => {
                setChartFilter('Mine');
                setInLocalStorage('chart', { tab: 'Mine' });
              }),
          },
        ]}
        buttons={[
          {
            name: (
              <>
                <i className="fa fa-plus" />
                {t('Chart')}
              </>
            ),
            buttonStyle: 'tertiary',
            onClick: () => {
              window.location.assign('/chart/add');
            },
          },
          {
            name: 'View All »',
            buttonStyle: 'link',
            onClick: () => {
              const target =
                chartFilter === 'Favorite'
                  ? '/chart/list/?filters=(favorite:!t)'
                  : '/chart/list/';
              history.push(target);
            },
          },
        ]}
      />
      {charts?.length ? (
        <CardContainer>
          {charts.map(e => (
            <ChartCard
              key={`${e.id}`}
              openChartEditModal={openChartEditModal}
              chartFilter={chartFilter}
              chart={e}
              userId={user?.userId}
              hasPerm={hasPerm}
              showThumbnails={showThumbnails}
              bulkSelectEnabled={bulkSelectEnabled}
              refreshData={refreshData}
              addDangerToast={addDangerToast}
              addSuccessToast={addSuccessToast}
              favoriteStatus={favoriteStatus[e.id]}
              saveFavoriteStatus={saveFavoriteStatus}
            />
          ))}
        </CardContainer>
      ) : (
        <EmptyState tableName="CHARTS" tab={chartFilter} />
      )}
    </ErrorBoundary>
  );
}

export default withToasts(ChartTable);
