import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { t } from '@superset-ui/core';
import { InfoTooltipWithTrigger } from '@superset-ui/chart-controls';

import Button from 'src/components/Button';
import { exploreChart } from 'src/explore/exploreUtils';
import * as actions from '../actions/sqlLab';

const propTypes = {
  actions: PropTypes.object.isRequired,
  table: PropTypes.string.isRequired,
  schema: PropTypes.string,
  dbId: PropTypes.number.isRequired,
  errorMessage: PropTypes.string,
  templateParams: PropTypes.string,
};

class ExploreCtasResultsButton extends React.PureComponent {
  constructor(props) {
    super(props);
    this.visualize = this.visualize.bind(this);
    this.onClick = this.onClick.bind(this);
  }

  onClick() {
    this.visualize();
  }

  buildVizOptions() {
    return {
      datasourceName: this.props.table,
      schema: this.props.schema,
      dbId: this.props.dbId,
      templateParams: this.props.templateParams,
    };
  }

  visualize() {
    this.props.actions
      .createCtasDatasource(this.buildVizOptions())
      .then(data => {
        const formData = {
          datasource: `${data.table_id}__table`,
          metrics: ['count'],
          groupby: [],
          viz_type: 'table',
          since: '100 years ago',
          all_columns: [],
          row_limit: 1000,
        };
        this.props.actions.addInfoToast(
          t('Creating a data source and creating a new tab'),
        );

        // open new window for data visualization
        exploreChart(formData);
      })
      .catch(() => {
        this.props.actions.addDangerToast(
          this.props.errorMessage || t('An error occurred'),
        );
      });
  }

  render() {
    return (
      <>
        <Button
          buttonSize="small"
          onClick={this.onClick}
          tooltip={t('Explore the result set in the data exploration view')}
        >
          <InfoTooltipWithTrigger
            icon="line-chart"
            placement="top"
            label="explore"
          />{' '}
          {t('Explore')}
        </Button>
      </>
    );
  }
}
ExploreCtasResultsButton.propTypes = propTypes;

function mapStateToProps({ sqlLab, common }) {
  return {
    errorMessage: sqlLab.errorMessage,
    timeout: common.conf ? common.conf.RABBITAI_WEBSERVER_TIMEOUT : null,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ExploreCtasResultsButton);
