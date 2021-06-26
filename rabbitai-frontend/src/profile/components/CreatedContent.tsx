
import React from 'react';
import moment from 'moment';
import { t } from '@rabbitai-ui/core';

import TableLoader from '../../components/TableLoader';
import { Slice } from '../types';
import { User, Dashboard } from '../../types/bootstrapTypes';

interface CreatedContentProps {
  user: User;
}

class CreatedContent extends React.PureComponent<CreatedContentProps> {
  renderSliceTable() {
    const mutator = (data: Slice[]) =>
      data.map(slice => ({
        slice: <a href={slice.url}>{slice.title}</a>,
        favorited: moment.utc(slice.dttm).fromNow(),
        _favorited: slice.dttm,
      }));
    return (
      <TableLoader
        dataEndpoint={`/rabbitai/created_slices/${this.props.user.userId}/`}
        className="table-condensed"
        columns={['slice', 'favorited']}
        mutator={mutator}
        noDataText={t('No charts')}
        sortable
      />
    );
  }

  renderDashboardTable() {
    const mutator = (data: Dashboard[]) =>
      data.map(dash => ({
        dashboard: <a href={dash.url}>{dash.title}</a>,
        favorited: moment.utc(dash.dttm).fromNow(),
        _favorited: dash.dttm,
      }));
    return (
      <TableLoader
        className="table-condensed"
        mutator={mutator}
        dataEndpoint={`/rabbitai/created_dashboards/${this.props.user.userId}/`}
        noDataText={t('No dashboards')}
        columns={['dashboard', 'favorited']}
        sortable
      />
    );
  }

  render() {
    return (
      <div>
        <h3>{t('Dashboards')}</h3>
        {this.renderDashboardTable()}
        <hr />
        <h3>{t('Charts')}</h3>
        {this.renderSliceTable()}
      </div>
    );
  }
}

export default CreatedContent;
