
/* eslint-disable no-unused-expressions */
import React from 'react';
import sinon from 'sinon';
import { shallow } from 'enzyme';

import AdhocFilter, {
  EXPRESSION_TYPES,
  CLAUSES,
} from 'src/explore/components/controls/FilterControl/AdhocFilter';
import { AGGREGATES } from 'src/explore/constants';
import AdhocMetric from 'src/explore/components/controls/MetricControl/AdhocMetric';
import AdhocFilterEditPopoverSimpleTabContent from '.';

const simpleAdhocFilter = new AdhocFilter({
  expressionType: EXPRESSION_TYPES.SIMPLE,
  subject: 'value',
  operator: '>',
  comparator: '10',
  clause: CLAUSES.WHERE,
});

const simpleMultiAdhocFilter = new AdhocFilter({
  expressionType: EXPRESSION_TYPES.SIMPLE,
  subject: 'value',
  operator: 'IN',
  comparator: ['10'],
  clause: CLAUSES.WHERE,
});

const sumValueAdhocMetric = new AdhocMetric({
  expressionType: EXPRESSION_TYPES.SIMPLE,
  column: { type: 'VARCHAR(255)', column_name: 'source' },
  aggregate: AGGREGATES.SUM,
});

const simpleCustomFilter = new AdhocFilter({
  expressionType: EXPRESSION_TYPES.SIMPLE,
  subject: 'ds',
  operator: 'LATEST PARTITION',
});

const options = [
  { type: 'VARCHAR(255)', column_name: 'source', id: 1 },
  { type: 'VARCHAR(255)', column_name: 'target', id: 2 },
  { type: 'DOUBLE', column_name: 'value', id: 3 },
  { saved_metric_name: 'my_custom_metric', id: 4 },
  sumValueAdhocMetric,
];

function setup(overrides) {
  const onChange = sinon.spy();
  const onHeightChange = sinon.spy();
  const props = {
    adhocFilter: simpleAdhocFilter,
    onChange,
    onHeightChange,
    options,
    datasource: {},
    ...overrides,
  };
  const wrapper = shallow(
    <AdhocFilterEditPopoverSimpleTabContent {...props} />,
  );
  return { wrapper, onChange, onHeightChange };
}

describe('AdhocFilterEditPopoverSimpleTabContent', () => {
  it('renders the simple tab form', () => {
    const { wrapper } = setup();
    expect(wrapper).toExist();
  });

  it('passes the new adhocFilter to onChange after onSubjectChange', () => {
    const { wrapper, onChange } = setup();
    wrapper.instance().onSubjectChange(1);
    expect(onChange.calledOnce).toBe(true);
    expect(onChange.lastCall.args[0]).toEqual(
      simpleAdhocFilter.duplicateWith({ subject: 'source' }),
    );
  });

  it('may alter the clause in onSubjectChange if the old clause is not appropriate', () => {
    const { wrapper, onChange } = setup();
    wrapper.instance().onSubjectChange(sumValueAdhocMetric.optionName);
    expect(onChange.calledOnce).toBe(true);
    expect(onChange.lastCall.args[0]).toEqual(
      simpleAdhocFilter.duplicateWith({
        subject: sumValueAdhocMetric.label,
        clause: CLAUSES.HAVING,
      }),
    );
  });

  it('will convert from individual comparator to array if the operator changes to multi', () => {
    const { wrapper, onChange } = setup();
    wrapper.instance().onOperatorChange('IN');
    expect(onChange.calledOnce).toBe(true);
    expect(onChange.lastCall.args[0]).toEqual(
      simpleAdhocFilter.duplicateWith({ operator: 'IN', comparator: ['10'] }),
    );
  });

  it('will convert from array to individual comparators if the operator changes from multi', () => {
    const { wrapper, onChange } = setup({
      adhocFilter: simpleMultiAdhocFilter,
    });
    wrapper.instance().onOperatorChange('<');
    expect(onChange.calledOnce).toBe(true);
    expect(onChange.lastCall.args[0]).toEqual(
      simpleMultiAdhocFilter.duplicateWith({ operator: '<', comparator: '10' }),
    );
  });

  it('passes the new adhocFilter to onChange after onComparatorChange', () => {
    const { wrapper, onChange } = setup();
    wrapper.instance().onComparatorChange('20');
    expect(onChange.calledOnce).toBe(true);
    expect(onChange.lastCall.args[0]).toEqual(
      simpleAdhocFilter.duplicateWith({ comparator: '20' }),
    );
  });

  it('will filter operators for table datasources', () => {
    const { wrapper } = setup({ datasource: { type: 'table' } });
    expect(wrapper.instance().isOperatorRelevant('REGEX')).toBe(false);
    expect(wrapper.instance().isOperatorRelevant('LIKE')).toBe(true);
  });

  it('will filter operators for druid datasources', () => {
    const { wrapper } = setup({ datasource: { type: 'druid' } });
    expect(wrapper.instance().isOperatorRelevant('REGEX')).toBe(true);
    expect(wrapper.instance().isOperatorRelevant('LIKE')).toBe(false);
  });

  it('will show LATEST PARTITION operator', () => {
    const { wrapper } = setup({
      datasource: {
        type: 'table',
        datasource_name: 'table1',
        schema: 'schema',
      },
      adhocFilter: simpleCustomFilter,
      partitionColumn: 'ds',
    });

    expect(
      wrapper.instance().isOperatorRelevant('LATEST PARTITION', 'ds'),
    ).toBe(true);
    expect(
      wrapper.instance().isOperatorRelevant('LATEST PARTITION', 'value'),
    ).toBe(false);
  });

  it('will generate custom sqlExpression for LATEST PARTITION operator', () => {
    const testAdhocFilter = new AdhocFilter({
      expressionType: EXPRESSION_TYPES.SIMPLE,
      subject: 'ds',
    });
    const { wrapper, onChange } = setup({
      datasource: {
        type: 'table',
        datasource_name: 'table1',
        schema: 'schema',
      },
      adhocFilter: testAdhocFilter,
      partitionColumn: 'ds',
    });

    wrapper.instance().onOperatorChange('LATEST PARTITION');
    expect(onChange.lastCall.args[0]).toEqual(
      testAdhocFilter.duplicateWith({
        subject: 'ds',
        operator: 'LATEST PARTITION',
        comparator: null,
        clause: 'WHERE',
        expressionType: 'SQL',
        sqlExpression: "ds = '{{ presto.latest_partition('schema.table1') }}'",
      }),
    );
  });
  it('will display boolean operators only when column type is boolean', () => {
    const { wrapper } = setup({
      datasource: {
        type: 'table',
        datasource_name: 'table1',
        schema: 'schema',
        columns: [{ column_name: 'value', type: 'BOOL' }],
      },
      adhocFilter: simpleAdhocFilter,
    });
    const booleanOnlyOperators = [
      'IS TRUE',
      'IS FALSE',
      'IS NULL',
      'IS NOT NULL',
    ];
    booleanOnlyOperators.forEach(operator => {
      expect(wrapper.instance().isOperatorRelevant(operator, 'value')).toBe(
        true,
      );
    });
  });
  it('will display boolean operators when column type is number', () => {
    const { wrapper } = setup({
      datasource: {
        type: 'table',
        datasource_name: 'table1',
        schema: 'schema',
        columns: [{ column_name: 'value', type: 'INT' }],
      },
      adhocFilter: simpleAdhocFilter,
    });
    const booleanOnlyOperators = ['IS TRUE', 'IS FALSE'];
    booleanOnlyOperators.forEach(operator => {
      expect(wrapper.instance().isOperatorRelevant(operator, 'value')).toBe(
        true,
      );
    });
  });
  it('will not display boolean operators when column type is string', () => {
    const { wrapper } = setup({
      datasource: {
        type: 'table',
        datasource_name: 'table1',
        schema: 'schema',
        columns: [{ column_name: 'value', type: 'STRING' }],
      },
      adhocFilter: simpleAdhocFilter,
    });
    const booleanOnlyOperators = ['IS TRUE', 'IS FALSE'];
    booleanOnlyOperators.forEach(operator => {
      expect(wrapper.instance().isOperatorRelevant(operator, 'value')).toBe(
        false,
      );
    });
  });
  it('will display boolean operators when column is an expression', () => {
    const { wrapper } = setup({
      datasource: {
        type: 'table',
        datasource_name: 'table1',
        schema: 'schema',
        columns: [
          {
            column_name: 'value',
            expression: 'case when value is 0 then "NO"',
          },
        ],
      },
      adhocFilter: simpleAdhocFilter,
    });
    const booleanOnlyOperators = ['IS TRUE', 'IS FALSE'];
    booleanOnlyOperators.forEach(operator => {
      expect(wrapper.instance().isOperatorRelevant(operator, 'value')).toBe(
        true,
      );
    });
  });
});
