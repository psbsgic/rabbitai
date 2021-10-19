import PropTypes from 'prop-types';
import { EXPRESSION_TYPES, CLAUSES } from './AdhocFilter';

export default PropTypes.oneOfType([
  PropTypes.shape({
    expressionType: PropTypes.oneOf([EXPRESSION_TYPES.SIMPLE]).isRequired,
    clause: PropTypes.oneOf([CLAUSES.HAVING, CLAUSES.WHERE]).isRequired,
    subject: PropTypes.string.isRequired,
    comparator: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.arrayOf(PropTypes.string),
    ]).isRequired,
  }),
  PropTypes.shape({
    expressionType: PropTypes.oneOf([EXPRESSION_TYPES.SQL]).isRequired,
    clause: PropTypes.oneOf([CLAUSES.WHERE, CLAUSES.HAVING]).isRequired,
    sqlExpression: PropTypes.string.isRequired,
  }),
]);
