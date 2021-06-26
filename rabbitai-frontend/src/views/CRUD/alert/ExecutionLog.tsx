

import { styled, t } from '@rabbitai-ui/core';
import moment from 'moment';
import React, { useEffect, useMemo } from 'react';
import { Link, useParams } from 'react-router-dom';
import ListView from 'src/components/ListView';
import SubMenu from 'src/components/Menu/SubMenu';
import withToasts from 'src/messageToasts/enhancers/withToasts';
import { fDuration } from 'src/modules/dates';
import AlertStatusIcon from 'src/views/CRUD/alert/components/AlertStatusIcon';
import {
  useListViewResource,
  useSingleViewResource,
} from 'src/views/CRUD/hooks';
import { AlertObject, LogObject } from './types';

const PAGE_SIZE = 25;

const StyledHeader = styled.div`
  display: flex;
  flex-direction: row;

  a,
  Link {
    margin-left: 16px;
    font-size: 12px;
    font-weight: normal;
    text-decoration: underline;
  }
`;

interface ExecutionLogProps {
  addDangerToast: (msg: string) => void;
  addSuccessToast: (msg: string) => void;
  isReportEnabled: boolean;
}

function ExecutionLog({ addDangerToast, isReportEnabled }: ExecutionLogProps) {
  const { alertId }: any = useParams();
  const {
    state: { loading, resourceCount: logCount, resourceCollection: logs },
    fetchData,
  } = useListViewResource<LogObject>(
    `report/${alertId}/log`,
    t('log'),
    addDangerToast,
    false,
  );
  const {
    state: { loading: alertLoading, resource: alertResource },
    fetchResource,
  } = useSingleViewResource<AlertObject>(
    'report',
    t('reports'),
    addDangerToast,
  );

  useEffect(() => {
    if (alertId !== null && !alertLoading) {
      fetchResource(alertId);
    }
  }, [alertId]);

  const initialSort = [{ id: 'start_dttm', desc: true }];
  const columns = useMemo(
    () => [
      {
        Cell: ({
          row: {
            original: { state },
          },
        }: any) => (
          <AlertStatusIcon state={state} isReportEnabled={isReportEnabled} />
        ),
        accessor: 'state',
        Header: t('State'),
        size: 'xs',
        disableSortBy: true,
      },
      {
        Cell: ({
          row: {
            original: { uuid: executionId },
          },
        }: any) => (executionId ? executionId.slice(0, 6) : 'none'),
        accessor: 'uuid',
        Header: t('Execution ID'),
        size: 'xs',
        disableSortBy: true,
      },
      {
        Cell: ({
          row: {
            original: { scheduled_dttm: scheduledDttm },
          },
        }: any) =>
          moment(new Date(scheduledDttm)).format('YYYY-MM-DD hh:mm:ss a'),
        accessor: 'scheduled_dttm',
        Header: t('Scheduled at (UTC)'),
      },
      {
        Cell: ({
          row: {
            original: { start_dttm: startDttm },
          },
        }: any) => moment(new Date(startDttm)).format('YYYY-MM-DD hh:mm:ss a'),
        Header: t('Start at (UTC)'),
        accessor: 'start_dttm',
      },
      {
        Cell: ({
          row: {
            original: { start_dttm: startDttm, end_dttm: endDttm },
          },
        }: any) =>
          fDuration(new Date(startDttm).getTime(), new Date(endDttm).getTime()),
        Header: t('Duration'),
        disableSortBy: true,
      },
      {
        accessor: 'value',
        Header: t('Value'),
      },
      {
        accessor: 'error_message',
        Header: t('Error message'),
      },
    ],
    [isReportEnabled],
  );
  const path = `/${isReportEnabled ? 'report' : 'alert'}/list/`;
  return (
    <>
      <SubMenu
        name={
          <StyledHeader>
            <span>
              {t(`${alertResource?.type}`)} {alertResource?.name}
            </span>
            <span>
              <Link to={path}>Back to all</Link>
            </span>
          </StyledHeader>
        }
      />
      <ListView<LogObject>
        className="execution-log-list-view"
        columns={columns}
        count={logCount}
        data={logs}
        fetchData={fetchData}
        initialSort={initialSort}
        loading={loading}
        pageSize={PAGE_SIZE}
      />
    </>
  );
}

export default withToasts(ExecutionLog);
