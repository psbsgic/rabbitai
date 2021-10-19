import React from 'react';
import PropTypes from 'prop-types';
import ButtonGroup from 'src/components/ButtonGroup';
import { t, useTheme } from '@superset-ui/core';

import { Tooltip } from 'src/components/Tooltip';
import Button from 'src/components/Button';

const propTypes = {
  canAdd: PropTypes.bool.isRequired,
  onQuery: PropTypes.func.isRequired,
  onSave: PropTypes.func,
  onStop: PropTypes.func,
  loading: PropTypes.bool,
  chartIsStale: PropTypes.bool,
  errorMessage: PropTypes.node,
};

const defaultProps = {
  onStop: () => {},
  onSave: () => {},
};

export default function QueryAndSaveBtns({
  canAdd,
  onQuery,
  onSave,
  onStop,
  loading,
  chartIsStale,
  errorMessage,
}) {
  let qryButtonStyle = 'tertiary';
  if (errorMessage) {
    qryButtonStyle = 'danger';
  } else if (chartIsStale) {
    qryButtonStyle = 'primary';
  }

  const saveButtonDisabled = errorMessage ? true : loading;
  const qryOrStopButton = loading ? (
    <Button
      onClick={onStop}
      buttonStyle="warning"
      buttonSize="small"
      disabled={!canAdd}
    >
      <i className="fa fa-stop-circle-o" /> {t('Stop')}
    </Button>
  ) : (
    <Button
      buttonSize="small"
      onClick={onQuery}
      buttonStyle={qryButtonStyle}
      disabled={!!errorMessage}
      data-test="run-query-button"
    >
      <i className="fa fa-bolt" /> {t('Run')}
    </Button>
  );

  const theme = useTheme();

  return (
    <div
      css={{
        display: 'flex',
        flexShrink: 0,
        flexDirection: 'row',
        alignItems: 'center',
        paddingTop: theme.gridUnit * 2,
        paddingRight: theme.gridUnit * 2,
        paddingBottom: 0,
        paddingLeft: theme.gridUnit * 4,
        '& button': {
          width: 100,
        },
        '.errMsg': {
          marginLeft: theme.gridUnit * 4,
        },
      }}
    >
      <ButtonGroup className="query-and-save">
        {qryOrStopButton}
        <Button
          buttonStyle="tertiary"
          buttonSize="small"
          data-target="#save_modal"
          data-toggle="modal"
          disabled={saveButtonDisabled}
          onClick={onSave}
          data-test="query-save-button"
        >
          <i className="fa fa-plus-circle" /> {t('Save')}
        </Button>
      </ButtonGroup>
      {errorMessage && (
        <span className="errMsg">
          {' '}
          <Tooltip
            id="query-error-tooltip"
            placement="right"
            title={errorMessage}
          >
            <i className="fa fa-exclamation-circle text-danger fa-lg" />
          </Tooltip>
        </span>
      )}
    </div>
  );
}

QueryAndSaveBtns.propTypes = propTypes;
QueryAndSaveBtns.defaultProps = defaultProps;
