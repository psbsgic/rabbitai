
import React from 'react';
import PropTypes from 'prop-types';
import { getNumberFormatter, t } from '@rabbitai-ui/core';

import Label from 'src/components/Label';
import { Tooltip } from 'src/components/Tooltip';

const propTypes = {
  rowcount: PropTypes.number,
  limit: PropTypes.number,
  rows: PropTypes.string,
  suffix: PropTypes.string,
  loading: PropTypes.bool,
};

const defaultProps = {
  suffix: t('rows'),
};

export default function RowCountLabel({ rowcount, limit, suffix, loading }) {
  const limitReached = rowcount === limit;
  const type =
    limitReached || (rowcount === 0 && !loading) ? 'danger' : 'default';
  const formattedRowCount = getNumberFormatter()(rowcount);
  const tooltip = (
    <span>
      {limitReached && <div>{t('Limit reached')}</div>}
      {loading ? 'Loading' : rowcount}
    </span>
  );
  return (
    <Tooltip id="tt-rowcount-tooltip" title={tooltip}>
      <Label type={type} data-test="row-count-label">
        {loading ? 'Loading...' : `${formattedRowCount} ${suffix}`}
      </Label>
    </Tooltip>
  );
}

RowCountLabel.propTypes = propTypes;
RowCountLabel.defaultProps = defaultProps;
