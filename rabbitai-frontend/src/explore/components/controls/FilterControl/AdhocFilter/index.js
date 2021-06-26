
import { CUSTOM_OPERATORS, OPERATORS } from 'src/explore/constants';
import { getSimpleSQLExpression } from 'src/explore/exploreUtils';

export const EXPRESSION_TYPES = {
  SIMPLE: 'SIMPLE',
  SQL: 'SQL',
};

export const CLAUSES = {
  HAVING: 'HAVING',
  WHERE: 'WHERE',
};

const OPERATORS_TO_SQL = {
  '==': '=',
  '!=': '<>',
  '>': '>',
  '<': '<',
  '>=': '>=',
  '<=': '<=',
  IN: 'IN',
  'NOT IN': 'NOT IN',
  LIKE: 'LIKE',
  ILIKE: 'ILIKE',
  REGEX: 'REGEX',
  'IS NOT NULL': 'IS NOT NULL',
  'IS NULL': 'IS NULL',
  'IS TRUE': 'IS TRUE',
  'IS FALSE': 'IS FALSE',
  'LATEST PARTITION': ({ datasource }) =>
    `= '{{ presto.latest_partition('${datasource.schema}.${datasource.datasource_name}') }}'`,
};

function translateToSql(adhocMetric, { useSimple } = {}) {
  if (adhocMetric.expressionType === EXPRESSION_TYPES.SIMPLE || useSimple) {
    const { subject, comparator } = adhocMetric;
    const operator =
      adhocMetric.operator && CUSTOM_OPERATORS.has(adhocMetric.operator)
        ? OPERATORS_TO_SQL[adhocMetric.operator](adhocMetric)
        : OPERATORS_TO_SQL[adhocMetric.operator];
    return getSimpleSQLExpression(subject, operator, comparator);
  }
  if (adhocMetric.expressionType === EXPRESSION_TYPES.SQL) {
    return adhocMetric.sqlExpression;
  }
  return '';
}

export default class AdhocFilter {
  constructor(adhocFilter) {
    this.expressionType = adhocFilter.expressionType || EXPRESSION_TYPES.SIMPLE;
    if (this.expressionType === EXPRESSION_TYPES.SIMPLE) {
      this.subject = adhocFilter.subject;
      this.operator = adhocFilter.operator?.toUpperCase();
      this.comparator = adhocFilter.comparator;
      this.clause = adhocFilter.clause || CLAUSES.WHERE;
      this.sqlExpression = null;
    } else if (this.expressionType === EXPRESSION_TYPES.SQL) {
      this.sqlExpression =
        typeof adhocFilter.sqlExpression === 'string'
          ? adhocFilter.sqlExpression
          : translateToSql(adhocFilter, { useSimple: true });
      this.clause = adhocFilter.clause;
      if (adhocFilter.operator && CUSTOM_OPERATORS.has(adhocFilter.operator)) {
        this.subject = adhocFilter.subject;
        this.operator = adhocFilter.operator;
      } else {
        this.subject = null;
        this.operator = null;
      }
      this.comparator = null;
    }
    this.isExtra = !!adhocFilter.isExtra;
    this.isNew = !!adhocFilter.isNew;

    this.filterOptionName =
      adhocFilter.filterOptionName ||
      `filter_${Math.random()
        .toString(36)
        .substring(2, 15)}_${Math.random().toString(36).substring(2, 15)}`;
  }

  duplicateWith(nextFields) {
    return new AdhocFilter({
      ...this,
      // all duplicated fields are not new (i.e. will not open popup automatically)
      isNew: false,
      ...nextFields,
    });
  }

  equals(adhocFilter) {
    return (
      adhocFilter.expressionType === this.expressionType &&
      adhocFilter.sqlExpression === this.sqlExpression &&
      adhocFilter.operator === this.operator &&
      adhocFilter.comparator === this.comparator &&
      adhocFilter.subject === this.subject
    );
  }

  isValid() {
    if (this.expressionType === EXPRESSION_TYPES.SIMPLE) {
      if (
        [
          OPERATORS['IS TRUE'],
          OPERATORS['IS FALSE'],
          OPERATORS['IS NULL'],
          OPERATORS['IS NOT NULL'],
        ].indexOf(this.operator) >= 0
      ) {
        return !!(this.operator && this.subject);
      }

      if (this.operator && this.subject && this.clause) {
        if (Array.isArray(this.comparator)) {
          if (this.comparator.length > 0) {
            // A non-empty array of values ('IN' or 'NOT IN' clauses)
            return true;
          }
        } else if (this.comparator !== null) {
          // A value has been selected or typed
          return true;
        }
      }
    } else if (this.expressionType === EXPRESSION_TYPES.SQL) {
      return !!(this.sqlExpression && this.clause);
    }
    return false;
  }

  getDefaultLabel() {
    const label = this.translateToSql();
    return label.length < 43 ? label : `${label.substring(0, 40)}...`;
  }

  getTooltipTitle() {
    return this.translateToSql();
  }

  translateToSql() {
    return translateToSql(this);
  }
}
