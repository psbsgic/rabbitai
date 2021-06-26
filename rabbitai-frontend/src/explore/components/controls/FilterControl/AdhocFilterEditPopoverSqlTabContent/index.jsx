
import React from 'react';
import PropTypes from 'prop-types';
import { NativeSelect as Select } from 'src/components/Select';
import { t } from '@rabbitai-ui/core';
import { SQLEditor } from 'src/components/AsyncAceEditor';
import sqlKeywords from 'src/SqlLab/utils/sqlKeywords';

import adhocMetricType from 'src/explore/components/controls/MetricControl/adhocMetricType';
import columnType from 'src/explore/components/controls/FilterControl/columnType';
import AdhocFilter, {
  EXPRESSION_TYPES,
  CLAUSES,
} from 'src/explore/components/controls/FilterControl/AdhocFilter';

const propTypes = {
  adhocFilter: PropTypes.instanceOf(AdhocFilter).isRequired,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.arrayOf(
    PropTypes.oneOfType([
      columnType,
      PropTypes.shape({ saved_metric_name: PropTypes.string.isRequired }),
      adhocMetricType,
    ]),
  ).isRequired,
  height: PropTypes.number.isRequired,
  activeKey: PropTypes.string.isRequired,
};

export default class AdhocFilterEditPopoverSqlTabContent extends React.Component {
  constructor(props) {
    super(props);
    this.onSqlExpressionChange = this.onSqlExpressionChange.bind(this);
    this.onSqlExpressionClauseChange = this.onSqlExpressionClauseChange.bind(
      this,
    );
    this.handleAceEditorRef = this.handleAceEditorRef.bind(this);

    this.selectProps = {
      name: 'select-column',
    };
  }

  componentDidUpdate() {
    if (this.aceEditorRef) {
      this.aceEditorRef.editor.resize();
    }
  }

  onSqlExpressionClauseChange(clause) {
    this.props.onChange(
      this.props.adhocFilter.duplicateWith({
        clause,
        expressionType: EXPRESSION_TYPES.SQL,
      }),
    );
  }

  onSqlExpressionChange(sqlExpression) {
    this.props.onChange(
      this.props.adhocFilter.duplicateWith({
        sqlExpression,
        expressionType: EXPRESSION_TYPES.SQL,
      }),
    );
  }

  handleAceEditorRef(ref) {
    if (ref) {
      this.aceEditorRef = ref;
    }
  }

  render() {
    const { adhocFilter, height, options } = this.props;

    const clauseSelectProps = {
      placeholder: t('choose WHERE or HAVING...'),
      value: adhocFilter.clause,
      onChange: this.onSqlExpressionClauseChange,
    };
    const keywords = sqlKeywords.concat(
      options
        .map(option => {
          if (option.column_name) {
            return {
              name: option.column_name,
              value: option.column_name,
              score: 50,
              meta: 'option',
            };
          }
          return null;
        })
        .filter(Boolean),
    );

    return (
      <span>
        <div className="filter-edit-clause-section">
          <Select
            {...this.selectProps}
            {...clauseSelectProps}
            className="filter-edit-clause-dropdown"
            getPopupContainer={triggerNode => triggerNode.parentNode}
          >
            {Object.keys(CLAUSES).map(clause => (
              <Select.Option value={clause} key={clause}>
                {clause}
              </Select.Option>
            ))}
          </Select>
          <span className="filter-edit-clause-info">
            <strong>WHERE</strong> {t('Filters by columns')}
            <br />
            <strong>HAVING</strong> {t('Filters by metrics')}
          </span>
        </div>
        <div css={theme => ({ marginTop: theme.gridUnit * 4 })}>
          <SQLEditor
            ref={this.handleAceEditorRef}
            keywords={keywords}
            height={`${height - 130}px`}
            onChange={this.onSqlExpressionChange}
            width="100%"
            showGutter={false}
            value={adhocFilter.sqlExpression || adhocFilter.translateToSql()}
            editorProps={{ $blockScrolling: true }}
            enableLiveAutocompletion
            className="filter-sql-editor"
            wrapEnabled
          />
        </div>
      </span>
    );
  }
}
AdhocFilterEditPopoverSqlTabContent.propTypes = propTypes;
