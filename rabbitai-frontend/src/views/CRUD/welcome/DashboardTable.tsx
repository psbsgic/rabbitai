
import React, { useState, useMemo, useEffect } from 'react';
import { RabbitaiClient, t } from '@rabbitai-ui/core';
import { useListViewResource, useFavoriteStatus } from 'src/views/CRUD/hooks';
import { Dashboard, DashboardTableProps } from 'src/views/CRUD/types';
import { useHistory } from 'react-router-dom';
import {
  setInLocalStorage,
  getFromLocalStorage,
} from 'src/utils/localStorageHelpers';
import withToasts from 'src/messageToasts/enhancers/withToasts';
import Loading from 'src/components/Loading';
import PropertiesModal from 'src/dashboard/components/PropertiesModal';
import DashboardCard from 'src/views/CRUD/dashboard/DashboardCard';
import SubMenu from 'src/components/Menu/SubMenu';
import EmptyState from './EmptyState';
import { createErrorHandler, CardContainer } from '../utils';

const PAGE_SIZE = 3;

export interface FilterValue {
  col: string;
  operator: string;
  value: string | boolean | number | null | undefined;
}

function DashboardTable({
  user,
  addDangerToast,
  addSuccessToast,
  mine,
  showThumbnails,
}: DashboardTableProps) {
  const history = useHistory();
  const {
    state: { loading, resourceCollection: dashboards },
    setResourceCollection: setDashboards,
    hasPerm,
    refreshData,
    fetchData,
  } = useListViewResource<Dashboard>(
    'dashboard',
    t('dashboard'),
    addDangerToast,
    true,
    mine,
    [],
    false,
  );
  const dashboardIds = useMemo(() => dashboards.map(c => c.id), [dashboards]);
  const [saveFavoriteStatus, favoriteStatus] = useFavoriteStatus(
    'dashboard',
    dashboardIds,
    addDangerToast,
  );
  const [editModal, setEditModal] = useState<Dashboard>();
  const [dashboardFilter, setDashboardFilter] = useState('Mine');

  useEffect(() => {
    const filter = getFromLocalStorage('dashboard', null);
    if (!filter) {
      setDashboardFilter('Mine');
    } else setDashboardFilter(filter.tab);
  }, []);

  const handleDashboardEdit = (edits: Dashboard) =>
    RabbitaiClient.get({
      endpoint: `/api/v1/dashboard/${edits.id}`,
    }).then(
      ({ json = {} }) => {
        setDashboards(
          dashboards.map(dashboard => {
            if (dashboard.id === json.id) {
              return json.result;
            }
            return dashboard;
          }),
        );
      },
      createErrorHandler(errMsg =>
        addDangerToast(
          t('An error occurred while fetching dashboards: %s', errMsg),
        ),
      ),
    );

  const getFilters = (filterName: string) => {
    const filters = [];
    if (filterName === 'Mine') {
      filters.push({
        id: 'owners',
        operator: 'rel_m_m',
        value: `${user?.userId}`,
      });
    } else {
      filters.push({
        id: 'id',
        operator: 'dashboard_is_favorite',
        value: true,
      });
    }
    return filters;
  };
  const subMenus = [];
  if (dashboards.length > 0 && dashboardFilter === 'favorite') {
    subMenus.push({
      name: 'Favorite',
      label: t('Favorite'),
      onClick: () => setDashboardFilter('Favorite'),
    });
  }

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
    <>
      <SubMenu
        activeChild={dashboardFilter}
        tabs={[
          {
            name: 'Favorite',
            label: t('Favorite'),
            onClick: () => {
              getData('Favorite').then(() => {
                setDashboardFilter('Favorite');
                setInLocalStorage('dashboard', { tab: 'Favorite' });
              });
            },
          },
          {
            name: 'Mine',
            label: t('Mine'),
            onClick: () => {
              getData('Mine').then(() => {
                setDashboardFilter('Mine');
                setInLocalStorage('dashboard', { tab: 'Mine' });
              });
            },
          },
        ]}
        buttons={[
          {
            name: (
              <>
                <i className="fa fa-plus" />
                Dashboard
              </>
            ),
            buttonStyle: 'tertiary',
            onClick: () => {
              window.location.assign('/dashboard/new');
            },
          },
          {
            name: 'View All »',
            buttonStyle: 'link',
            onClick: () => {
              const target =
                dashboardFilter === 'Favorite'
                  ? '/dashboard/list/?filters=(favorite:!t)'
                  : '/dashboard/list/';
              history.push(target);
            },
          },
        ]}
      />
      {editModal && (
        <PropertiesModal
          dashboardId={editModal?.id}
          show
          onHide={() => setEditModal(undefined)}
          onSubmit={handleDashboardEdit}
        />
      )}
      {dashboards.length > 0 && (
        <CardContainer>
          {dashboards.map(e => (
            <DashboardCard
              key={e.id}
              dashboard={e}
              hasPerm={hasPerm}
              bulkSelectEnabled={false}
              showThumbnails={showThumbnails}
              dashboardFilter={dashboardFilter}
              refreshData={refreshData}
              addDangerToast={addDangerToast}
              addSuccessToast={addSuccessToast}
              userId={user?.userId}
              loading={loading}
              openDashboardEditModal={(dashboard: Dashboard) =>
                setEditModal(dashboard)
              }
              saveFavoriteStatus={saveFavoriteStatus}
              favoriteStatus={favoriteStatus[e.id]}
            />
          ))}
        </CardContainer>
      )}
      {dashboards.length === 0 && (
        <EmptyState tableName="DASHBOARDS" tab={dashboardFilter} />
      )}
    </>
  );
}

export default withToasts(DashboardTable);
