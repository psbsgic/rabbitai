import React from 'react';
import Label from 'src/components/Label';

import { STATE_TYPE_MAP } from '../constants';
import { Query } from '../types';

interface QueryStateLabelProps {
  query: Query;
}

export default function QueryStateLabel({ query }: QueryStateLabelProps) {
  return (
    <Label className="m-r-3" type={STATE_TYPE_MAP[query.state]}>
      {query.state}
    </Label>
  );
}
