
import React from 'react';
import moment from 'moment';
import { t } from '@rabbitai-ui/core';

import TableLoader from '../../components/TableLoader';
import { Slice } from '../types';
import { User, Dashboard } from '../../types/bootstrapTypes';

interface FavoritesProps {
  user: User;
}

export default class Favorites extends React.PureComponent<FavoritesProps> {
  renderSliceTable() {
    const mutator = (data: Slice[]) =>
      data.map(slice => ({
        slice: <a href={slice.url}>{slice.title}</a>,
        creator: <a href={slice.creator_url}>{slice.creator}</a>,
        favorited: moment.utc(slice.dttm).fromNow(),
        _favorited: slice.dttm,
      }));
    return (
      <TableLoader
        dataEndpoint={`/rabbitai/fave_slices/${this.props.user.userId}/`}
        className="table-condensed"
        columns={['slice', 'creator', 'favorited']}
        mutator={mutator}
        noDataText={t('No favorite charts yet, go click on stars!')}
        sortable
      />
    );
  }

  renderDashboardTable() {
    const mutator = (data: Dashboard[]) =>
      data.map(dash => ({
        dashboard: <a href={dash.url}>{dash.title}</a>,
        creator: <a href={dash.creator_url}>{dash.creator}</a>,
        favorited: moment.utc(dash.dttm).fromNow(),
      }));
    return (
      <TableLoader
        className="table-condensed"
        mutator={mutator}
        dataEndpoint={`/rabbitai/fave_dashboards/${this.props.user.userId}/`}
        noDataText={t('No favorite dashboards yet, go click on stars!')}
        columns={['dashboard', 'creator', 'favorited']}
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
