import React from 'react';
import moment from 'moment';

import TableLoader from '../../components/TableLoader';
import { Activity } from '../types';
import { User } from '../../types/bootstrapTypes';

interface RecentActivityProps {
  user: User;
}

export default function RecentActivity({ user }: RecentActivityProps) {
  const rowLimit = 50;
  const mutator = function (data: Activity[]) {
    return data
      .filter(row => row.action === 'dashboard' || row.action === 'explore')
      .map(row => ({
        name: <a href={row.item_url}>{row.item_title}</a>,
        type: row.action,
        time: moment.utc(row.time).fromNow(),
        _time: row.time,
      }));
  };
  return (
    <div>
      <TableLoader
        className="table-condensed"
        mutator={mutator}
        sortable
        dataEndpoint={`/rabbitai/recent_activity/${user.userId}/?limit=${rowLimit}`}
      />
    </div>
  );
}
