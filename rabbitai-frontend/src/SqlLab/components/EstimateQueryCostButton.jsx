
import React, { useMemo } from 'react';
import PropTypes from 'prop-types';
import Alert from 'src/components/Alert';
import { t } from '@rabbitai-ui/core';

import TableView from 'src/components/TableView';
import Button from 'src/components/Button';
import Loading from '../../components/Loading';
import ModalTrigger from '../../components/ModalTrigger';
import { EmptyWrapperType } from '../../components/TableView/TableView';

const propTypes = {
  dbId: PropTypes.number.isRequired,
  schema: PropTypes.string.isRequired,
  sql: PropTypes.string.isRequired,
  getEstimate: PropTypes.func.isRequired,
  queryCostEstimate: PropTypes.Object,
  selectedText: PropTypes.string,
  tooltip: PropTypes.string,
  disabled: PropTypes.bool,
};
const defaultProps = {
  queryCostEstimate: [],
  tooltip: '',
  disabled: false,
};

const EstimateQueryCostButton = props => {
  const { cost } = props.queryCostEstimate;
  const tableData = useMemo(() => (Array.isArray(cost) ? cost : []), [cost]);
  const columns = useMemo(
    () =>
      Array.isArray(cost) && cost.length
        ? Object.keys(cost[0]).map(key => ({ accessor: key, Header: key }))
        : [],
    [cost],
  );

  const onClick = () => {
    props.getEstimate();
  };

  const renderModalBody = () => {
    if (props.queryCostEstimate.error !== null) {
      return (
        <Alert
          key="query-estimate-error"
          type="error"
          message={props.queryCostEstimate.error}
        />
      );
    }
    if (props.queryCostEstimate.completed) {
      return (
        <TableView
          columns={columns}
          data={tableData}
          withPagination={false}
          emptyWrapperType={EmptyWrapperType.Small}
          className="cost-estimate"
        />
      );
    }
    return <Loading position="normal" />;
  };

  const { disabled, selectedText, tooltip } = props;
  const btnText = selectedText
    ? t('Estimate selected query cost')
    : t('Estimate cost');
  return (
    <span className="EstimateQueryCostButton">
      <ModalTrigger
        modalTitle={t('Cost estimate')}
        modalBody={renderModalBody()}
        triggerNode={
          <Button
            style={{ height: 32, padding: '4px 15px' }}
            onClick={onClick}
            key="query-estimate-btn"
            tooltip={tooltip}
            disabled={disabled}
          >
            {btnText}
          </Button>
        }
      />
    </span>
  );
};

EstimateQueryCostButton.propTypes = propTypes;
EstimateQueryCostButton.defaultProps = defaultProps;

export default EstimateQueryCostButton;
